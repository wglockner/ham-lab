

/*

Author: Walter W Glockner
Date: 2/3/2024
ROS2 to Arduino control

*/

#include <P1AM.h>

#include <ArduinoRS485.h>
#include <ArduinoModbus.h>

#include <SL4848CR.h>

//#include <ros2arduino.h>
//#include <user_config.h>

//#include <Ethernet.h>

#define BAUD_RATE 9600


bool initialized = false;
short currentProcessValue;
short currentSetPointValue;
int currentAutoTuningState;
int ros2Data[128];

void setup()
{
  // Begin Serial connection
  Serial.begin(BAUD_RATE);
  // Start Modbus Client
  ModbusRTUClientInit(BAUD_RATE);
}

void loop()
{
  getRos2Data();

  if(!initialized)
  {
    // Set Control Mode from ros2
    setControlMode(ros2Data[0],ros2Data[0]);
    currentProcessValue = getProcessValue(ros2Data[0]);

    // Set process Point Value from ros2
    setSetPointValue(1, ros2Data[0]);
    currentSetPointValue = getSetPointValue(ros2Data[0]);

    // Set Auto Tuning from ros2
    setAutoTuning(ros2Data[0]);
    currentAutoTuningState = getAutoTuningState(ros2Data[0]);

    initialized = true;
    }
    else{
      Serial.println ("Initialized");
    }
}

// Collect data from ros2
void getRos2Data()
{
  // some mechanism to collect data from ros2
  for(int i=0; i = 127; i++)
  {
  ros2Data[i] = 0; // REPLACE WITH ROSS DATA COLLECTION!!!!!!!!!!!!! 
  Serial.print(ros2Data[i]);
  }
}


