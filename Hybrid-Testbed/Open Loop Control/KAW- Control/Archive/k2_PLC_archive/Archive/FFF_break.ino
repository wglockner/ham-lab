#include <SL4848CR.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>
#include <Extruder.h>
#include <P1AM.h>
Extruder E;


void setup(){
  Serial.begin(9600);
  while(!Serial){
    ;
  }
  while(!P1.init()){
    ;
  }
  Serial.println("- P1 modules initialized");

  while(!ModbusRTUClientInit(9600)){
    ;
  }
  Serial.println("- Modbus initialized");
  
  while(!SL4848CRInit(1,9600,0,466.667, 0.0, -17)){
    ;
  }
  Serial.println("- Heaters Initialized");
  E.setAcceleration(10);
}

void loop(){

  //set feedrate


}