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
---Clearcore boots without analog input causing unprompted extrusion.

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
char incomingByte;
bool stopFlag = false;



void setup() {
  // Instance of Extruder and SL4848-CR heater
  Serial.begin(9600);

  while (!P1.init())
    ;
  while (!ModbusClientKAW.init())
    ;
  extruderMotorEnable = extruderData[0];
  heater1Address = heater1Data[0];
  Heater1.init(1, 0);
  Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
}

void loop() {
  ////////////////////////////////////////////////
  // Gather Data from the serial command window.//  
  ////////////////////////////////////////////////

  if (Serial.available() > 0) {
    incomingByte = Serial.read();
  }

  // If Serial is S or s, Stop extrusion and robot movement
  if ((incomingByte == 'S') || (incomingByte == 's')) {
    Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
    Serial.println("- Extrusion Stopped!");
    stopFlag = true;

  }

  // If there is no stop flag then extrude
  if (!stopFlag) {

    
    Extrude(220, 0);
    Serial.println("Extruding");

  }
  // Continue extrusion if g or G is entered as serial command ('G'O)
  else if ((incomingByte == 'g')||(incomingByte == 'G')){
    stopFlag = !stopFlag;
  }

  // If f or F is entered, increase the flowrate
  if ((incomingByte == 'f') || (incomingByte == 'F')) {
    Extruder.setExtrudeFlowrate(Extruder.getExtrudeFlowrate() + 100);
    Serial.print("- New Flowrate: ");
    Serial.println(Extruder.getExtrudeFlowrate());
    
  }

  // If d or D is entered in serial window, decease flowrate
  else if ((incomingByte == 'd') || (incomingByte == 'D')) {
    Extruder.setExtrudeFlowrate(Extruder.getExtrudeFlowrate() - 100);
    Serial.print("- New Flowrate: ");
    Serial.println(Extruder.getExtrudeFlowrate());
    }
  }

// Extrude plastic at feedrate
bool Extrude(float extruderTemp, float flowrate) {

  // If the extruder was extruding, 
  if (!Extruder.getWasExtruding()) {

    Extruder.setExtrudeFlowrate(flowrate);
    setMotorSignal();
    Serial.print ("motorSignal: ");
    Serial.println (motorSignal);
    Serial.print("Flowrate: ");
    Serial.println(Extruder.getExtrudeFlowrate());

    // Set extruder temperature Parameters
    Heater1.setSetPointValue(heater1Address, extruderTemp);

    while (!Heater1.atTemp(heater1Address)){
    ;
    }

    // Wait for Serial command of y/n to start extrusion or not
    Serial.println("Start Print?(y/n)");
    while (!Serial.available()) {
      ;
    }
    incomingByte = Serial.read();
    

    if (incomingByte == 'y') {
      // Turn on motor
      Serial.println("Extruding");
      while (!Extruder.setEnableMotor(motorSignal, extrusionMotorAnalogPin, kawGoesMOOvePin))
        ;
      P1.writeDiscrete(HIGH, kawGoesMOOvePin);
      Extruder.setWasExtruding();
      incomingByte = 0;
    }
  }
  else{

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
void setMotorSignal(){ 
  motorSignal = (Extruder.getExtrudeFlowrate() / 840 + 1) * 2048;
}
