/*

Author: Walter W Glockner
Date: 3/7/2024

Description:
This sketch facilitates plastic FFF processes for
The Kawasaki robot, P1AM-200 PLC, ClearCore controller
Clearpath motor, SL4848-CR PID controller, and their 
respective paripherals. The Kawasaki Library included in
this sketch and its dependencies are necessarry for this
sketch.  

Current known problem: 

Potential solution: 
Use a normally open relay for the power of the Clearcore
and only supply power once a discrete output from the P1AM-200 is written


Current known problem: 
---Speed setting is buggy and works sometimes and not others.

Potential solution:
Cross check the clearcore input with the motor signal value and smooth
when necessarry

Current known problem:
---Occationally a serial communication will not be read by the P1AM-200
---have not yet written retraction or data update.


*/

#include <Kawasaki_FFF.h>
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0x60, 0x52, 0xD0, 0x07, 0x7F, 0xCB };
IPAddress ip(192, 168, 1, 2);
EthernetServer server(10000);

Extruder Extruder;
SL4848CR Heater1;
ModbusClientKAW ModbusClientKAW;
signed int extruderData[25] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
signed int heater1Data[25] = { 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
int extruderMotorEnable;
signed int extrudeFlowrate;
signed int retractFlowrate;
float extruderTemp;
int motorSignal;
int heater1Address;
channelLabel kawGoesMOOvePin = { 3, 1 };
channelLabel extrusionMotorAnalogPin = { 7, 1 };
channelLabel clearPin = { 3, 15 };

channelLabel airPin = { 4, 2 };
char incomingByte;
bool stopFlag = 0;



void setup() {
  // Instance of Extruder and SL4848-CR heater
  Serial.begin(9600);
  while (!Serial)
    ;

  while (!P1.init())
    ;

  Ethernet.begin(mac, ip);
  server.begin();

  while (!ModbusClientKAW.init())
    ;
  extruderMotorEnable = extruderData[0];
  heater1Address = heater1Data[0];
  Heater1.init(1, 0);
  Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
  P1.writeDiscrete(HIGH, airPin);

  //client.println("Setup Complete");
}

void loop() {
  ////////////////////////////////////////////////
  // Gather Data from the serial command window.//
  ////////////////////////////////////////////////

  EthernetClient client = server.available();
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
  }
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        client.println(c);




        // If Serial is S or s, Stop extrusion and robot movement
        if ((c == 'S') || (c == 's')) {
          Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
          client.write("- Extrusion Stopped! (S)");
          client.println("- Extrusion Stopped!");
          stopFlag = true;
        }

        // If there is no stop flag then extrude
        if (!stopFlag) {

          Extrude(160, -600);
        } else if ((c == 'g') || (c == 'G')) {
          stopFlag = !stopFlag;
        }

        // Continue extrusion if g or G is entered as serial command ('G'O)
        if (stopFlag) {
          if ((c == 'g') || (c == 'G')) {
            stopFlag = !stopFlag;
          }
        }

        // If f or F is entered, increase the flowrate
        if ((c == 'f') || (c == 'F')) {
          Extruder.setExtrudeFlowrate(Extruder.getExtrudeFlowrate() + 100);
          client.print("- New Flowrate: ");
          client.println(Extruder.getExtrudeFlowrate());
        }

        // If d or D is entered in serial window, decease flowrate
        if ((c == 'd') || (c == 'D')) {
          Extruder.setExtrudeFlowrate(Extruder.getExtrudeFlowrate() - 100);
          client.print("- New Flowrate: ");
          client.println(Extruder.getExtrudeFlowrate());
        }
      }
    }
  }
  client.stop();
}

// Extrude plastic at feedrate
bool Extrude(float extruderTemp, float flowrate) {

  EthernetClient client = server.available();

  // If the extruder was extruding,
  if (!Extruder.getWasExtruding()) {

    Extruder.setExtrudeFlowrate(flowrate);
    setMotorSignal();
    client.print("motorSignal: ");
    client.println(motorSignal);
    client.print("Flowrate: ");
    client.println(Extruder.getExtrudeFlowrate());

    // Set extruder temperature Parameters
    Heater1.setSetPointValue(heater1Address, extruderTemp);

    while (!Heater1.atTemp(heater1Address)) {
      ;
    }

    // Wait for Serial command of y/n to start extrusion or not
    client.println("Start Print?(y/n)");
    while (!Serial.available()) {
      ;
    }
    incomingByte = Serial.read();
    char c = client.read();


    if (c == 'y') {
      // Turn on motor
      client.println("Extruding");
      while (!Extruder.setEnableMotor(motorSignal, extrusionMotorAnalogPin, kawGoesMOOvePin))
        ;
      P1.writeDiscrete(HIGH, kawGoesMOOvePin);
      P1.writeDiscrete(HIGH, clearPin);
      Extruder.setWasExtruding();
      c = 0;
    }
  } else {

    Extruder.setEnableMotor(Extruder.getExtrudeFlowrate(), extrusionMotorAnalogPin, kawGoesMOOvePin);
    P1.writeDiscrete(HIGH, kawGoesMOOvePin);
    return true;
  }
}

bool retract() {
  return true;
};
bool updateData() {
  for (int i = 0; i < 25; i++) {
    extruderData[i] = extruderData[i];
    heater1Data[i] = heater1Data[i];
  }
}
void setMotorSignal() {
  motorSignal = (Extruder.getExtrudeFlowrate() / 840 + 1) * 2048;
}
