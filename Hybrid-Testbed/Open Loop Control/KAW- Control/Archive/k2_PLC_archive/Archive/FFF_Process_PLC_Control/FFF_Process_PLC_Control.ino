#include <Kawasaki_FFF.h>
Extruder Extruder;
SL4848CR Heater1;
ModbusClientKAW ModbusClientKAW;
signed int extruderData[25] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
signed int heater1Data[25] = { 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
int extruderMotorEnable;
int extrudeFlowrate;
int retractFlowrate;
int extruderTemp;
float motorSignal;
int heater1Address;
channelLabel kawGoesMOOvePin = { 3, 1 };
channelLabel extrusionMotorAnalogPin = { 7, 1 };
char incomingByte;
bool pauseFlag = 0;
int counter = 0;


void setup() {
  // Instance of Extruder and SL4848-CR heater
  Serial.begin(9600);

  while (!P1.init())
    ;
  while (!ModbusClientKAW.init())
    ;

  extruderMotorEnable = extruderData[0];
  extrudeFlowrate = extruderData[1];
  retractFlowrate = extruderData[2];
  extruderTemp = heater1Data[1];
  heater1Address = heater1Data[0];
  Heater1.init(1, 0);
  Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
}

void loop() {
  

  if (Serial.available() > 0) {
    incomingByte = Serial.read();
  }
  // If Serial is P or p, pause extrusion and robot movement
  if ((incomingByte == 'p') || (incomingByte == 'P')) {
    Extruder.stopEMotor(kawGoesMOOvePin, extrusionMotorAnalogPin);
    Serial.println("- Extrusion Paused!");
    pauseFlag = true;

  }
  if (!pauseFlag) {
    
    Extrude(220, Extruder.getExtrudeFlowrate());
  }

  // Pause if p is entered as serial command
  if (pauseFlag) {
    if (incomingByte == 's'){
      pauseFlag = !pauseFlag;
    }
  }


  if ((incomingByte == 'f') || (incomingByte == 'F')) {
    extrudeFlowrate= extrudeFlowrate + 100;
    Serial.print("- New Flowrate: ");
    Serial.println(extrudeFlowrate);
    
  }

if ((incomingByte == 'd') || (incomingByte == 'D')) {
    extrudeFlowrate= extrudeFlowrate - 100;
    Serial.print("- New Flowrate: ");
    Serial.println(extrudeFlowrate);

  }

}

// Extrude plastic at feedrate
bool Extrude(float extruderTemp, float flowrate) {

  if (!Extruder.getWasExtruding()) {

    Extruder.setExtrudeFlowrate(flowrate);
    motorSignal = (Extruder.getExtrudeFlowrate() / 840 + 1) * 2048;
    Serial.print ("motorSignal: ");
    Serial.println (motorSignal);
    Serial.print("Flowrate: ");
    Serial.println(Extruder.getExtrudeFlowrate());
    
    //Extruder.setExtrudeFlowrate(motorSignal);

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

      //motorSignal = (Extruder.getExtrudeFlowrate() / 840 + 1) * 2048;
      //Extruder.setExtrudeFlowrate(motorSignal);

      Extruder.setEnableMotor(Extruder.getExtrudeFlowrate(), extrusionMotorAnalogPin, kawGoesMOOvePin);
      Serial.println(Extruder.getExtrudeFlowrate());

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
