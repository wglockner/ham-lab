// Walter W Glockner

#include <Kawasaki_FFF.h>
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0x60, 0x52, 0xD0, 0x07, 0x7F, 0xCB }; // MAC address of P1AM-ETH module
byte ip[] = { 192, 168, 1, 2 }; // IP address of P1AM-ETH module
byte server[] = { 192, 168, 1, 1 }; // IP address of the server

EthernetClient client;

struct DeviceState {
    float extrudeFlowrate = 0.0, extruderTemp = 0.0;
    bool isPrinting = false, isPaused = false, startFlag;
    bool automated = false;
} extruderState;

Extruder Extruder;
SL4848CR Heater1;
ModbusClientKAW ModbusClientKAW;
unsigned long lastIOSendTime = 0;
const unsigned long ioUpdateInterval = 50; // Milliseconds

signed int extruderData[25];
signed int heater1Data[25];
int extruderMotorEnable = 0;

int heater1Address = 1;
float eMotorRPM = 0.0;
float layerHeight = 0.0;
float firstLayerHeight = 0.0;
float defaultLineWidth = 0.0;
float firstLayerLineWidth = 0.0;

bool isClientConnected = false;
bool wasClientConnected = false;
bool isGuiConnected = false;

uint32_t outputStates[9];  // Array to store the state of output pins
channelLabel kawGoesMOOvePin = { 3, 1 };
channelLabel extrusionMotorAnalogPin = { 7, 1 };
channelLabel clearPin = { 3, 9 };
channelLabel airPin = { 4, 2 };
channelLabel airAdjustPin = { 7, 8 };
channelLabel extrusionPin = { 2, 10 };
channelLabel retractionPin = { 2, 11 };
const int rumblerPin = 2; // No channel because GPIO module
int channel, pin, state;

String incomingByte = ""; // Changed to String
bool stopFlag = 0;

void setup() {
    Serial.begin(9600);
    delay(100);
    while (!P1.init());
    Ethernet.begin(mac, ip);
    delay(1000);

    initializeHardware();

    Serial.print("P1AM-ETH at IP:");
    Serial.println("Connecting...");

    if (client.connect(server, 10000)) {
        Serial.println("Connected");
        isClientConnected = true;
    } else {
        Serial.println("Connection Failed");
    }
}

void initializeHardware() {
    // Stop extrusion motor
    Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
    // Initialize all P1AM outputs to LOW
    P1.writeDiscrete(LOW, airPin);
    // Set heater temps to 0

    // Initialize Modbus
    while (!ModbusClientKAW.init());
    // Wait until initializations have completed before turning on ClearCore
    Heater1.setSetPointValue(heater1Address, 0);
    delay(3000);
    P1.writeDiscrete(HIGH, clearPin);
}

void serverListen() {
    if (client.available()) {
        while (client.available()) {
            char c = client.read();
            Serial.print("Received: ");  // Debugging statement
            Serial.println(c);
            // Accumulate characters until a newline is found
            if (c != '\r' && c != '\n') {
                incomingByte += c;
            } else if (c == '\n') {
                Serial.print("Complete Command: ");
                Serial.println(incomingByte);
                handleCommand(incomingByte, client);
                incomingByte = ""; // Reset the string for the next command
            }
        }
    }

    if (!client.connected()) {
        Serial.println("Client disconnected.");
        client.stop();
        isClientConnected = false;
    }
}

void handleOutputCommand(int channel, int pin, bool state) {
    P1.writeDiscrete(state, channel, pin);  // Assuming P1 is a method or object dealing with I/O
    Serial.print("Output set on channel ");
    Serial.print(channel);
    Serial.print(", pin ");
    Serial.print(pin);
    Serial.println(state ? " HIGH" : " LOW");
}

void handleCommand(String command, EthernetClient &client) {
    Serial.print("Handling command: ");  // Debugging statement
    Serial.println(command);

    if (command.startsWith("SET_OUTPUT:")) {
        if (sscanf(command.c_str(), "SET_OUTPUT:%d:%d:%d", &channel, &pin, &state) == 3) {
            handleOutputCommand(channel, pin, state);
            client.println("Output command processed.");
        } else {
            client.println("Invalid output command.");
        }
        return;
    }

    if (command == "command:start_print") {
        if (!extruderState.isPrinting) {
            extruderState.isPrinting = true;
            extruderState.startFlag = true;
            P1.writeAnalog((2048 / 800) * Extruder.getExtrudeFlowrate() + 2048, extrusionMotorAnalogPin);
            Serial.println((2048 / 800) * Extruder.getExtrudeFlowrate() + 2048);
            P1.writeDiscrete(HIGH, kawGoesMOOvePin);
            client.println("Print started.");
            Serial.println("Print started.");
        } else {
            client.println("Print already in progress.");
            Serial.println("Print already in progress.");
            P1.writeAnalog((2048 / 800) * Extruder.getExtrudeFlowrate() + 2048, extrusionMotorAnalogPin);
            Serial.println((2048 / 800) * Extruder.getExtrudeFlowrate() + 2048);
        }
    } else if (command == "command:stop_print") {
        if (extruderState.isPrinting) {
            extruderState.isPrinting = false;
            extruderState.startFlag = false;
            P1.writeAnalog(2048, extrusionMotorAnalogPin);
            P1.writeDiscrete(LOW, kawGoesMOOvePin);
            client.println("Print stopped.");
            Serial.println("Print stopped.");
        } else {
            client.println("No print to stop.");
            Serial.println("No print to stop.");
        }
    } else if (command == "command:pause_print") {
        if (extruderState.isPrinting && !extruderState.isPaused) {
            extruderState.isPaused = true;
            P1.writeAnalog(2048, extrusionMotorAnalogPin);
            P1.writeDiscrete(LOW, kawGoesMOOvePin);
            client.println("Print paused.");
            Serial.println("Print paused.");
        } else {
            client.println("Print already paused or not started.");
            Serial.println("Print already paused or not started.");
        }
    } else if (command == "command:resume_print") {
        if (!extruderState.isPrinting && extruderState.isPaused) {
            extruderState.isPrinting = true;
            extruderState.isPaused = false;
            P1.writeAnalog((2048 / 800) * Extruder.getExtrudeFlowrate() + 2048, extrusionMotorAnalogPin);
            Serial.println((2048 / 800) * Extruder.getExtrudeFlowrate());
            P1.writeDiscrete(HIGH, kawGoesMOOvePin);
            client.println("Print resumed.");
            Serial.println("Print resumed.");
        } else {
            client.println("Print not paused or already running.");
            Serial.println("Print not paused or already running.");
        }
    }
    parseVariable(command, client); // Ensure parseVariable is declared before usage
}

void parseVariable(String command, EthernetClient &client) {
    int separatorPos = command.indexOf(':');
    if (separatorPos != -1) {
        String variableName = command.substring(0, separatorPos);
        String valueStr = command.substring(separatorPos + 1);

        if (variableName == "extrudeFlowrate") {
            extruderState.extrudeFlowrate = valueStr.toFloat();
            Extruder.setExtrudeFlowrate(extruderState.extrudeFlowrate);
            Serial.print("Extrude Flowrate set:");
            Serial.println(extruderState.extrudeFlowrate);
        } else if (variableName == "temperature") {
            extruderState.extruderTemp = valueStr.toFloat();
            Heater1.setSetPointValue(heater1Address, extruderState.extruderTemp);
            Serial.print("Extruder temperature set to: ");
            Serial.println(extruderState.extruderTemp);
        } else if (variableName == "air") {
            P1.writeDiscrete(valueStr == "on" ? HIGH : LOW, airPin);
        } else if (variableName == "automated") {
            extruderState.automated = valueStr == "on";
        } else if (variableName == "eMotorRPM") {
            eMotorRPM = valueStr.toFloat();
            Extruder.setExtrudeFlowrate(eMotorRPM);
            Serial.print("Extrude flowrate set to: ");
            Serial.println(eMotorRPM);
        } else if (variableName == "layer_height") {
            layerHeight = valueStr.toFloat();
            Serial.print("Layer height set to: ");
            Serial.println(layerHeight);
        } else if (variableName == "first_layer_height") {
            firstLayerHeight = valueStr.toFloat();
            Serial.print("First layer height set to: ");
            Serial.println(firstLayerHeight);
        } else if (variableName == "default_line_width") {
            defaultLineWidth = valueStr.toFloat();
            Serial.print("Default line width set to: ");
            Serial.println(defaultLineWidth);
        } else if (variableName == "first_layer_line_width") {
            firstLayerLineWidth = valueStr.toFloat();
            Serial.print("First layer line width set to: ");
            Serial.println(firstLayerLineWidth);
        } else if (variableName == "rumbler") {
            analogWrite(rumblerPin, valueStr == "off" ? 0 : 1);
            Serial.println("Toggled Rumbler");
        } else if (variableName == "stop_client") {
            client.stop();
            isClientConnected = false;
            Serial.println("Client stopped.");
        } else {
            Serial.print("Unknown variable: ");
            Serial.println(variableName);
        }
    }
}

void loop() {
    serverListen();
    if (extruderState.isPrinting) {
        P1.writeAnalog((2048.0 / 800.0) * Extruder.getExtrudeFlowrate() + 2048.0, extrusionMotorAnalogPin);
        Serial.println((2048.0 / 800.0) * Extruder.getExtrudeFlowrate() + 2048.0);
        P1.writeDiscrete(HIGH, kawGoesMOOvePin);
    }

    if (client.connected()) {
        serverListen();
    } else if (!isClientConnected) {
        Serial.println("Attempting to reconnect...");
        if (client.connect(server, 10000)) {
            Serial.println("Reconnected");
            isClientConnected = true;
        } else {
            Serial.println("Reconnection failed");
            delay(5000);  // Wait before retrying
        }
    }
}

void sendIODigitalSignals(EthernetClient &client) {
    String channel_1_states = "channel_1_states:";
    String channel_2_states = "channel_2_states:";
    for (int channel = 1; channel <= 2; channel++) {
        for (int pin = 1; pin <= 16; pin++) {
            bool state = P1.readDiscrete({ channel, pin });
            if (channel == 1) {
                channel_1_states += state ? "1" : "0";
                if (pin != 16) {
                    channel_1_states += ",";
                }
            }
            if (channel == 2) {
                channel_2_states += state ? "1" : "0";
                if (pin != 16) {
                    channel_2_states += ",";
                }
            }
        }
    }
    Serial.println(channel_1_states);  // Debugging statement
    Serial.println(channel_2_states);  // Debugging statement
    if (client.connected()) {
        client.println(channel_1_states + "\n" + channel_2_states + "\n");
    }
}

void setOutputState(int channel, int pin, bool state) {
    P1.writeDiscrete(state, channel, pin);
    Serial.print("Set output for Channel ");
    Serial.print(channel);
    Serial.print(", Pin ");
    Serial.print(pin);
    Serial.println(state ? " HIGH" : " LOW");
}
