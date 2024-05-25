Installing the Board:

1) Start the Arduino IDE and select File > Preferences.
2) Enter https://raw.githubusercontent.com/facts-engineering/facts-engineering.github.io/master/package_productivity-P1AM-boardmanagermodule_index.json 
   into the Additional Board Manager URLs field. You can add multiple URLs, separating them with commas.
3) Use Arduino's Boards Manager to install the board. Tools > Board > Boards Manager.
4) Type P1AM into the search box and click the install button.


#include <Kawasaki_FFF.h>
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0x60, 0x52, 0xD0, 0x07, 0x7F, 0xCB };
IPAddress ip(192, 168, 1, 2);
EthernetServer server(10000);

Extruder Extruder;
SL4848CR Heater1;
ModbusClientKAW ModbusClientKAW;
unsigned long lastIOSendTime = 0;
const unsigned long ioUpdateInterval = 2000;  // 2000 milliseconds = 2 seconds
signed int extruderData[25];
signed int heater1Data[25];
int extruderMotorEnable = 0;
float extrudeFlowrate = 0.0;
float retractFlowrate = 0.0;
float extruderTemp = 0.0;
float motorSignal;
int heater1Address = 1;
float eMotorRPM = 0.0;
float layerHeight = 0.0;
float firstLayerHeight = 0.0;
float defaultLineWidth = 0.0;
float firstLayerLineWidth = 0.0;
bool isPrinting = false;
bool isPaused = false;
bool wasExtruding = false;
bool wasRetracting = false;
bool startFlag;
bool automated = true;
bool isClientConnected = false;
bool wasClientConnected = false;
bool isGuiConnected = false;

uint32_t outputStates[9]; // Array to store the state of output pins
channelLabel kawGoesMOOvePin = { 3, 1 };
channelLabel extrusionMotorAnalogPin = { 7, 1 };
channelLabel clearPin = { 3, 9 };
channelLabel airPin = { 4, 2 };
channelLabel airAdjustPin = { 7, 8 };
channelLabel extrusionPin = { 2, 10 };
channelLabel retractionPin = { 2, 11 };
const int rumblerPin = 2;

char incomingByte;
bool stopFlag = 0;


void setup() {
  Serial.begin(9600);
  delay(100);
  
  while (!P1.init());
  pinMode(2,OUTPUT);
  Ethernet.begin(mac, ip);
  server.begin();
  Serial.println("Server is setup and waiting for connections...");
  while (!ModbusClientKAW.init());

  extruderMotorEnable = extruderData[0];
  for (int i = 0; i < 9; i++) {
    outputStates[i] = false;  // Initialize all outputs to LOW
    pinMode(i, OUTPUT);       // Set all pin modes to OUTPUT (if directly controlling pins)
  }
  Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
  Heater1.setSetPointValue(heater1Address, 0);
  P1.writeDiscrete(LOW, airPin);
  P1.writeDiscrete(HIGH, clearPin);
}
void sendIODigitalSignals(EthernetClient& client) {
  String ioMessage = "IO:";
  for (int i = 9; i <= 16; i++) {  // Ensure it loops from 9 to 16
    ioMessage += P1.readDiscrete({2, i}) ? "1" : "0";
    if (i < 16) {
      ioMessage += ",";  // Add comma as delimiter except after the last pin
    }
  }
  ioMessage += "\n";  // End the message with a newline

  if (client.connected()) {
    client.print(ioMessage);
    Serial.println(ioMessage);
  }
}

void setOutputState(uint32_t pin, bool state) {

  for(uint32_t j = 3; j <= 4; j++){
    for (uint32_t i = 9; i <= 16; i++) {  // Ensure it loops from 9 to 16
      P1.writeDiscrete(state, {j, i}) ? "1" : "0";
    }
  }
}


void sendOutputDigitalSignals(EthernetClient& client) {
  String message = "OUTPUT:";
  for (int i = 0; i < 8; i++) {
    bool state = readOutputState(i); // Hypothetical function to get the output state
    message += state ? "1" : "0";
    if (i < 8 - 1) {
      message += ",";
    }
  }
  message += "\n";

  if (client.connected()) {
    client.print(message);
    Serial.println(message);
  }
}


bool shouldSendUpdate() {
  unsigned long currentTime = millis();
  if (currentTime - lastIOSendTime >= ioUpdateInterval) {
    lastIOSendTime = currentTime;
    return true;
  }
  return false;
}

EthernetClient client;
void loop(){
EthernetClient newClient = server.available();
  if (newClient && !isClientConnected) {
    Serial.println("New client connected.");
    client = newClient;
    isClientConnected = true;
  }

  if (isClientConnected && client.connected()) {
    String currentLine = "";
    while (client.available()) {
      char c = client.read();
      if (c == '\n' && currentLine.length() > 0) {
        Serial.print("Received: ");
        Serial.println(currentLine);
        processClientInput(currentLine, client);
        currentLine = "";
      } else if (c != '\n') {
        currentLine += c;
      }
    }
    
    // Check if it's time to send an IO update
    if (shouldSendUpdate()) {
      sendIODigitalSignals(client);
    }
  }

  if (isClientConnected && !client.connected()) {
    Serial.println("Client disconnected.");
    client.stop();
    isClientConnected = false;
  }
}

void processClientInput(String currentLine, EthernetClient& client) {
  // Example command from GUI: "SET_OUTPUT:5:1" to set output 5 high
  if (currentLine.startsWith("SET_OUTPUT:")) {
    int separatorPos1 = currentLine.indexOf(':', 11);
    int separatorPos2 = currentLine.indexOf(':', separatorPos1 + 1);
    int pin = currentLine.substring(11, separatorPos1).toInt();
    bool state = currentLine.substring(separatorPos1 + 1, separatorPos2).toInt() == 1;
    setOutputState(pin, state); // Hypothetical function to set the output state
  }
}



// Command handling function
void handleCommand(String command, EthernetClient &client) {
  Serial.println(command);

  if (command == "start_print") {
    if (!isPrinting) {
      isPrinting = true;
      startFlag = true;
      Extruder.setEnableMotor(Extruder.getExtrudeFlowrate(), extrusionMotorAnalogPin, kawGoesMOOvePin);
      P1.writeDiscrete(HIGH, kawGoesMOOvePin);
      client.println("Print started.");
      Serial.println("Print started.");
    } else {
      client.println("Print already in progress.");
      Serial.println("Print already in progress.");
    }
  } else if (command == "stop_print") {
    if (isPrinting) {
      isPrinting = false;
      startFlag = false;
      P1.writeAnalog(2048, extrusionMotorAnalogPin);
      P1.writeAnalog(LOW, kawGoesMOOvePin);
      client.println("Print stopped.");
      Serial.println("Print stopped.");
    } else {
      client.println("No print to stop.");
      Serial.println("No print to stop.");
    }
  } else if (command == "pause_print") {
    if (isPrinting && !isPaused) {
      isPaused = true;
      P1.writeAnalog(2048, extrusionMotorAnalogPin);
      P1.writeAnalog(LOW, kawGoesMOOvePin);
      client.println("Print paused.");
      Serial.println("Print paused.");
    } else {
      client.println("Print already paused or not started.");
      Serial.println("Print already paused or not started.");
    }
  } else if (command == "resume_print") {
    if (!isPrinting && isPaused) {
      isPrinting = true;
      isPaused = false;
      Extruder.setEnableMotor(Extruder.getExtrudeFlowrate(), extrusionMotorAnalogPin, kawGoesMOOvePin);
      P1.writeDiscrete(HIGH, kawGoesMOOvePin);
      client.println("Print resumed.");
      Serial.println("Print resumed.");
    } else {
      client.println("Print not paused or already running.");
      Serial.println("Print not paused or already running.");
    }
  }
  // Add other command handling as necessary
}

void parseVariable(String variableName, String valueStr, EthernetClient &client) {
  if (variableName == "extrudeFlowrate") {
    extrudeFlowrate = valueStr.toFloat();
    Extruder.setExtrudeFlowrate(extrudeFlowrate);
  } else if (variableName == "temperature") {
    extruderTemp = valueStr.toFloat();
    Heater1.setSetPointValue(heater1Address, extruderTemp);
  } else if (variableName == "air") {
    P1.writeDiscrete(valueStr == "on" ? HIGH : LOW, airPin);
  } else if (variableName == "automated") {
    automated = valueStr == "on";
  } else if (variableName == "eMotorRPM") {
    eMotorRPM = valueStr.toFloat();
    Extruder.setExtrudeFlowrate(eMotorRPM);
  } else if (variableName == "layer_height") {
    layerHeight = valueStr.toFloat();
  } else if (variableName == "first_layer_height") {
    firstLayerHeight = valueStr.toFloat();
  } else if (variableName == "default_line_width") {
    defaultLineWidth = valueStr.toFloat();
  } else if (variableName == "first_layer_line_width") {
    firstLayerLineWidth = valueStr.toFloat();
  } else if (variableName == "rumbler") {
    analogWrite(rumblerPin, valueStr == "on" ? 500 : 0);
  } else if (variableName == "stop_client") {
    Serial.println("Client stop requested.");
    client.stop();
    isClientConnected = false;
  }
  // Add any additional variable handling as needed
}

void setMotorSignal() {
  if (startFlag) {
    motorSignal = (Extruder.getExtrudeFlowrate() / 840 + 1) * 2048;
    Serial.println(motorSignal);
    P1.writeAnalog(motorSignal, extrusionMotorAnalogPin);
  }
}


bool Extrude(float extruderTemp, float flowrate) {
  // Implementation based on your specific needs.
  return true;
}

bool retract() {
  // Implement retract functionality.
  return true;
}

bool updateData() {
  // Update the data based on your requirements.
  return true;
}
