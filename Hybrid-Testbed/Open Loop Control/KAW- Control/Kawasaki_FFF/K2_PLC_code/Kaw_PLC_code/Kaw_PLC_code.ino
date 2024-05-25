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
const unsigned long ioUpdateInterval = 50;  // 2000 milliseconds = 2 seconds
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

uint32_t outputStates[9];  // Array to store the state of output pins
channelLabel kawGoesMOOvePin = { 3, 1 };
channelLabel extrusionMotorAnalogPin = { 7, 1 };
channelLabel clearPin = { 3, 9 };
channelLabel airPin = { 4, 2 };
channelLabel airAdjustPin = { 7, 8 };
channelLabel extrusionPin = { 2, 10 };
channelLabel retractionPin = { 2, 11 };
const int rumblerPin = 2;
int channel, pin, state;
int randNumber1;
int randNumber2;
int randNumberCoinToss;
int randCounter = 0;
 int lightDelay = 175;

char incomingByte;
bool stopFlag = 0;

void setup() {
  Serial.begin(9600);
  delay(100);
  while (!P1.init())
    ;
  Ethernet.begin(mac, ip);
  server.begin();


  
  while (!ModbusClientKAW.init())
    ;




  extruderMotorEnable = extruderData[0];



  

  Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
  Heater1.setSetPointValue(heater1Address, 0);
  P1.writeDiscrete(LOW, airPin);
  P1.writeDiscrete(HIGH, clearPin);






  Serial.print("New IP Address: ");
  Serial.println(Ethernet.localIP());



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
  Serial.println(command);

  //int channel, pin, state;

  if (command.startsWith("SET_OUTPUT:")) {
    if (sscanf(command.c_str(), "SET_OUTPUT:%d:%d:%d", &channel, &pin, &state) == 3) {
      handleOutputCommand(channel, pin, state);
      client.println("Output command processed.");
    } else {
      client.println("Invalid output command.");
    }
    return;
  }

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
}


  void loop() {


    
  EthernetClient client = server.available();
  static String currentLine = "";  // Declare currentLine as static to persist across loop calls
  if (client) {
    if (!isClientConnected) {
      Serial.println("Client Connected");
      isClientConnected = true;
      currentLine = "";
    }

    // Debugging: Check for any byte available
    while (client.available()) {
      char c = client.read();
      Serial.print(c);  // Output every character received for debugging

      if (c == '\n') {
        Serial.println("Received newline character.");
        if (currentLine == "REQUEST_IO_UPDATE") {
          sendIODigitalSignals(client);  // Send the IO state update immediately upon request
        }
        if (currentLine.startsWith("SET_OUTPUT:")) {
          int channel, pin, state;
          if (sscanf(currentLine.c_str(), "SET_OUTPUT:%d:%d:%d", &channel, &pin, &state) == 3) {
            handleOutputCommand(channel, pin, state);
            client.println("Output command processed.");
          }
        }
          

        int separatorPos = currentLine.indexOf(':');
        if (separatorPos != -1) {
          String variableName = currentLine.substring(0, separatorPos);
          String valueStr = currentLine.substring(separatorPos + 1);
          parseVariable(variableName, valueStr, client);
        }
        currentLine = "";  // Reset currentLine after processing
      } else if (c != '\r') {
        currentLine += c;  // Accumulate the line until newline is found
      }
    }

    if (currentLine == "GUI_CONNECTED") {
      client.println("ACK_CONNECTED");  // Acknowledge connection
      isGuiConnected = true;
      isClientConnected = true;
      Serial.println("GUI successfully connected.");
    }
  } else {
    //Serial.println("No client connected.");
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
    client.stop();
    isClientConnected = false;
  }
}
