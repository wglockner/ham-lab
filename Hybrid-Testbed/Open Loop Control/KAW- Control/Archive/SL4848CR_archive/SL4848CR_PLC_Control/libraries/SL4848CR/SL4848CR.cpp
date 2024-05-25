/**

Author: Walter W Glockner
Date:2/3/2024


---------------REQUIRED-------------
P1AM-200 Board (must paste link from ProductivityOpen P1AM Repository)
P1AM.h library
ArduinoRS485.h library
ArduinoModbus.h library
SL4848_register_Addresses.h library 


Contents:

This sketch contains all necessarry functions required for the use of 
the SL4848-CR heater with the P1AM-200 PLC.

Included with this sketch is a library containing the register adresses
for the SL4848-CR.

*/

#include "SL4848CR.h"
#include <ArduinoRS485.h> // ArduinoModbus depends on the ArduinoRS485 library
#include <ArduinoModbus.h>
#include <P1AM.h> //include P1AM-200 PLC library

const uint16_t PROCESS_VALUE_ADDR = 0x1000; 
const uint16_t SET_POINT_VALUE_ADDR = 0x1001;
const uint16_t INPUT_RANGE_HIGH_ADDR = 0x1002;
const uint16_t INPUT_RANGE_LOW_ADDR = 0x1003;
const uint16_t INPUT_TYPE_ADDR = 0x1004;
const uint16_t CONTROL_MODE_ADDR = 0x1005;
const uint16_t HEATING_COOLING_ADDR = 0x1006;
const uint16_t OUTPUT_1_HEATING_PERIOD_ADDR = 0x1007;
const uint16_t OUTPUT_1_COOLING_PERIOD_ADDR = 0x1007;
const uint16_t OUTPUT_2_PERIOD_ADDR = 0x1008;
const uint16_t PROPORTION_BAND_ADDR = 0x1009;
const uint16_t INTEGRAL_TIME_ADDR = 0x100A;
const uint16_t DERIVATIVE_TIME_ADDR = 0x100B;
const uint16_t INTEGRAL_OFFSET_ADDR = 0x100C;
const uint16_t PD_CONTROL_OFFSET_ADDR = 0x100D;
const uint16_t PROPORTION_BAND_COEFFICIENT_ADDR = 0x100E;
const uint16_t DEAD_BAND_ADDR = 0x100F;
const uint16_t HEATING_HYSTERESIS_ADDR = 0x1010;
const uint16_t COOLING_HYSTERESIS_ADDR = 0x1011;
const uint16_t OUTPUT_1_LEVEL_ADDR = 0x1012;
const uint16_t OUTPUT_2_LEVEL_ADDR = 0x1013;
const uint16_t ANALOG_HIGH_ADJUSTMENT_ADDR = 0x1014;
const uint16_t ANALOG_LOW_ADJUSTMENT_ADDR = 0x1015;
const uint16_t PV_OFFSET_ADDR = 0x1016;
const uint16_t DECIMAL_POINT_POSITION_ADDR = 0x1017; 
const uint16_t PID_PARAMETER_GROUP_ADDR = 0x101C;
const uint16_t TARGET_SV_ADDR = 0x101D;
const uint16_t ALARM_1_ADDR = 0x1020;
const uint16_t ALARM_2_ADDR = 0x1021;
const uint16_t ALARM_3_ADDR = 0x1022;
const uint16_t SYSTEM_ALARM_ADDR = 0x1023;
const uint16_t ALARM_1_HIGH_LIMIT_ADDR = 0x1024; 
const uint16_t ALARM_1_LOW_LIMIT_ADDR = 0x1025;
const uint16_t ALARM_2_HIGH_LIMIT_ADDR = 0x1026; 
const uint16_t ALARM_2_LOW_LIMIT_ADDR = 0x1027;
const uint16_t ALARM_3_HIGH_LIMIT_ADDR = 0x1028;
const uint16_t ALARM_3_LOW_LIMIT_ADDR = 0x1029;
const uint16_t LED_STATUS_ADDR = 0x102A;
const uint16_t PUSHBUTTON_STATUS_ADDR = 0x102B;
const uint16_t LOCK_MODE_ADDR = 0x102C;
const uint16_t FIRMWARE_VERSION_ADDR = 0x102F;
const uint16_t STARTING_RAMP_SOAK_PATTERN_ADDR = 0x1030;

const uint16_t LAST_STEP_NUMBER_PATTERN_0_ADDR = 0x1040;
const uint16_t LAST_STEP_NUMBER_PATTERN_1_ADDR = 0x1041;
const uint16_t LAST_STEP_NUMBER_PATTERN_2_ADDR = 0x1042;
const uint16_t LAST_STEP_NUMBER_PATTERN_3_ADDR = 0x1043;
const uint16_t LAST_STEP_NUMBER_PATTERN_4_ADDR = 0x1044;
const uint16_t LAST_STEP_NUMBER_PATTERN_5_ADDR = 0x1045;
const uint16_t LAST_STEP_NUMBER_PATTERN_6_ADDR = 0x1046;
const uint16_t LAST_STEP_NUMBER_PATTERN_7_ADDR = 0x1047;

const uint16_t ADDITIONAL_CYCLES_PATTERN_0_ADDR = 0x1050;
const uint16_t ADDITIONAL_CYCLES_PATTERN_1_ADDR = 0x1051;
const uint16_t ADDITIONAL_CYCLES_PATTERN_2_ADDR = 0x1052;
const uint16_t ADDITIONAL_CYCLES_PATTERN_3_ADDR = 0x1053;
const uint16_t ADDITIONAL_CYCLES_PATTERN_4_ADDR = 0x1054;
const uint16_t ADDITIONAL_CYCLES_PATTERN_5_ADDR = 0x1055;
const uint16_t ADDITIONAL_CYCLES_PATTERN_6_ADDR = 0x1056;
const uint16_t ADDITIONAL_CYCLES_PATTERN_7_ADDR = 0x1057;

const uint16_t NEXT_PATTERN_NUMBER_PATTERN_0_ADDR = 0x1060;
const uint16_t NEXT_PATTERN_NUMBER_PATTERN_1_ADDR = 0x1061;
const uint16_t NEXT_PATTERN_NUMBER_PATTERN_2_ADDR = 0x1062;
const uint16_t NEXT_PATTERN_NUMBER_PATTERN_3_ADDR = 0x1063;
const uint16_t NEXT_PATTERN_NUMBER_PATTERN_4_ADDR = 0x1064;
const uint16_t NEXT_PATTERN_NUMBER_PATTERN_5_ADDR = 0x1065;
const uint16_t NEXT_PATTERN_NUMBER_PATTERN_6_ADDR = 0x1066;
const uint16_t NEXT_PATTERN_NUMBER_PATTERN_7_ADDR = 0x1067;

const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_0_ADDR = 0x2000;
const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_1_ADDR = 0x2001;
const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_2_ADDR = 0x2002;
const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_3_ADDR = 0x2003;
const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_4_ADDR = 0x2004;
const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_5_ADDR = 0x2005;
const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_6_ADDR = 0x2006;
const uint16_t RAMP_SOAK_SV_PATTERN_0_STEP_7_ADDR = 0x2007;

const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_0_ADDR = 0x2008;
const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_1_ADDR = 0x2009;
const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_2_ADDR = 0x200A;
const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_3_ADDR = 0x200B;
const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_4_ADDR = 0x200C;
const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_5_ADDR = 0x200D;
const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_6_ADDR = 0x200E;
const uint16_t RAMP_SOAK_SV_PATTERN_1_STEP_7_ADDR = 0x200F;

const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_0_ADDR = 0x2010;
const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_1_ADDR = 0x2011;
const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_2_ADDR = 0x2012;
const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_3_ADDR = 0x2013;
const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_4_ADDR = 0x2014;
const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_5_ADDR = 0x2015;
const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_6_ADDR = 0x2016;
const uint16_t RAMP_SOAK_SV_PATTERN_2_STEP_7_ADDR = 0x2017;

const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_0_ADDR = 0x2018;
const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_1_ADDR = 0x2019;
const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_2_ADDR = 0x201A;
const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_3_ADDR = 0x201B;
const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_4_ADDR = 0x201C;
const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_5_ADDR = 0x201D;
const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_6_ADDR = 0x201E;
const uint16_t RAMP_SOAK_SV_PATTERN_3_STEP_7_ADDR = 0x201F;

const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_0_ADDR = 0x2020;
const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_1_ADDR = 0x2021;
const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_2_ADDR = 0x2022;
const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_3_ADDR = 0x2023;
const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_4_ADDR = 0x2024;
const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_5_ADDR = 0x2025;
const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_6_ADDR = 0x2026;
const uint16_t RAMP_SOAK_SV_PATTERN_4_STEP_7_ADDR = 0x2027;

const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_0_ADDR = 0x2028;
const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_1_ADDR = 0x2029;
const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_2_ADDR = 0x202A;
const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_3_ADDR = 0x202B;
const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_4_ADDR = 0x202C;
const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_5_ADDR = 0x202D;
const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_6_ADDR = 0x202E;
const uint16_t RAMP_SOAK_SV_PATTERN_5_STEP_7_ADDR = 0x202F;

const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_0_ADDR = 0x2030;
const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_1_ADDR = 0x2031;
const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_2_ADDR = 0x2032;
const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_3_ADDR = 0x2033;
const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_4_ADDR = 0x2034;
const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_5_ADDR = 0x2035;
const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_6_ADDR = 0x2036;
const uint16_t RAMP_SOAK_SV_PATTERN_6_STEP_7_ADDR = 0x2037;

const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_0_ADDR = 0x2038;
const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_1_ADDR = 0x2039;
const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_2_ADDR = 0x203A;
const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_3_ADDR = 0x203B;
const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_4_ADDR = 0x203C;
const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_5_ADDR = 0x203D;
const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_6_ADDR = 0x203E;
const uint16_t RAMP_SOAK_SV_PATTERN_7_STEP_7_ADDR = 0x203F;


const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_0_ADDR = 0x2080;
const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_1_ADDR = 0x2081;
const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_2_ADDR = 0x2082;
const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_3_ADDR = 0x2083;
const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_4_ADDR = 0x2084;
const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_5_ADDR = 0x2085;
const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_6_ADDR = 0x2086;
const uint16_t RAMP_SOAK_TIME_PATTERN_0_STEP_7_ADDR = 0x2087;

const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_0_ADDR = 0x2088;
const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_1_ADDR = 0x2089;
const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_2_ADDR = 0x208A;
const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_3_ADDR = 0x208B;
const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_4_ADDR = 0x208C;
const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_5_ADDR = 0x208D;
const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_6_ADDR = 0x208E;
const uint16_t RAMP_SOAK_TIME_PATTERN_1_STEP_7_ADDR = 0x208F;

const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_0_ADDR = 0x2090;
const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_1_ADDR = 0x2091;
const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_2_ADDR = 0x2092;
const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_3_ADDR = 0x2093;
const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_4_ADDR = 0x2094;
const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_5_ADDR = 0x2095;
const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_6_ADDR = 0x2096;
const uint16_t RAMP_SOAK_TIME_PATTERN_2_STEP_7_ADDR = 0x2097;

const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_0_ADDR = 0x2098;
const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_1_ADDR = 0x2099;
const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_2_ADDR = 0x209A;
const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_3_ADDR = 0x209B;
const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_4_ADDR = 0x209C;
const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_5_ADDR = 0x209D;
const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_6_ADDR = 0x209E;
const uint16_t RAMP_SOAK_TIME_PATTERN_3_STEP_7_ADDR = 0x209F;

const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_0_ADDR = 0x20A0;
const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_1_ADDR = 0x20A1;
const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_2_ADDR = 0x20A2;
const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_3_ADDR = 0x20A3;
const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_4_ADDR = 0x20A4;
const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_5_ADDR = 0x20A5;
const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_6_ADDR = 0x20A6;
const uint16_t RAMP_SOAK_TIME_PATTERN_4_STEP_7_ADDR = 0x20A7;

const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_0_ADDR = 0x20A8;
const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_1_ADDR = 0x20A9;
const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_2_ADDR = 0x20AA;
const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_3_ADDR = 0x20AB;
const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_4_ADDR = 0x20AC;
const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_5_ADDR = 0x20AD;
const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_6_ADDR = 0x20AE;
const uint16_t RAMP_SOAK_TIME_PATTERN_5_STEP_7_ADDR = 0x20AF;

const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_0_ADDR = 0x20B0;
const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_1_ADDR = 0x20B1;
const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_2_ADDR = 0x20B2;
const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_3_ADDR = 0x20B3;
const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_4_ADDR = 0x20B4;
const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_5_ADDR = 0x20B5;
const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_6_ADDR = 0x20B6;
const uint16_t RAMP_SOAK_TIME_PATTERN_6_STEP_7_ADDR = 0x20B7;

const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_0_ADDR = 0x20B8;
const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_1_ADDR = 0x20B9;
const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_2_ADDR = 0x20BA;
const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_3_ADDR = 0x20BB;
const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_4_ADDR = 0x20BC;
const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_5_ADDR = 0x20BD;
const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_6_ADDR = 0x20BE;
const uint16_t RAMP_SOAK_TIME_PATTERN_7_STEP_7_ADDR = 0x20BF;

const uint16_t AT_LED_STATUS_ADDR = 0x0800;
const uint16_t OUTPUT_1_LED_STATUS_ADDR = 0x0801;
const uint16_t OUTPUT_2_LED_STATUS_ADDR = 0x0802;
const uint16_t ALARM_1_LED_STATUS_ADDR = 0x0803;
const uint16_t F_LED_STATUS_ADDR = 0x0804;
const uint16_t C_LED_STATUS_ADDR = 0x0805;
const uint16_t ALARM_2_LED_STATUS_ADDR = 0x0806; 
const uint16_t ALARM_3_LED_STATUS_ADDR = 0x0807;
const uint16_t SET_KEY_STATUS_ADDR = 0x0808;
const uint16_t FUNCTION_KEY_STATUS_ADDR = 0x0809;
const uint16_t UP_KEY_STATUS_ADDR = 0x080A;
const uint16_t DOWN_KEY_STATUS_ADDR = 0x080B;
const uint16_t EVENT_1_INPUT_STATUS_ADDR = 0x080C;
const uint16_t EVENT_2_INPUT_STATUS_ADDR = 0x080D;
const uint16_t SYSTEM_ALARM_STATUS_ADDR = 0x080E;
const uint16_t RAMP_SOAK_CONTROL_STATUS_ADDR = 0x080F;
const uint16_t ON_LINE_CONFIGURATION_ADDR = 0x0810;
const uint16_t TEMPERATURE_UNIT_DISPLAY_SELECTION_ADDR = 0x0811;
const uint16_t DECIMAL_POINT_DISPLAY_SELECTION_ADDR = 0x0812;
const uint16_t AUTO_TUNING_ADDR = 0x0813;
const uint16_t RUN_STOP_THE_CONTROL_ADDR = 0x0814;
const uint16_t STOP_THE_RAMP_SOAK_CONTROL_ADDR = 0x0815;
const uint16_t HOLD_THE_RAMP_SOAK_CONTROL_ADDR = 0x0816;

/////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////


// Initialize parameters for SL4848-CR
bool SL4848CRInit(int slaveID, int controlMode)
{
  // Start Serial Communication
  while(!Serial);

  // Set Control Mode
  while(!setControlMode(slaveID,controlMode));

  // Set Input Range to temp transmitter specs
  while(!setInputRange(slaveID));

  // Set PV offset
  while(!setPVOffset(slaveID, PVOffset));
  return true;
};


// Start Modbus RTU Client
bool ModbusRTUClientInit()
{
  // Wait for Serial connection
  while(!Serial);
  Serial.println("- Modbus RTU Client Toggle");

  // Error handling 
 if (!ModbusRTUClient.begin(9600)) {
    Serial.println("- Failed to start Modbus RTU Client!");
    return false;
  }
  
  // Confirm start of Modbus RTU Client
  else
  {
    Serial.println("- Successfully started Modbus RTU Client");
    return true;
  }
};


// Set Control Mode Parameter
bool setControlMode(int slaveID, int mode)
{
  switch (mode)
  {
    case 0:
      if (!ModbusRTUClient.holdingRegisterWrite(slaveID, CONTROL_MODE_ADDR, 0)) 
      {
        // Error handling
        Serial.println("- Failed to write Control Mode: PID! " + slaveID);
        Serial.println(ModbusRTUClient.lastError());
        return false;
      }
      else
      {
        setDecimalPointDisplaySelection(slaveID, 0);
        return true;
      }
      break;
    case 1:
      if (!ModbusRTUClient.holdingRegisterWrite(slaveID, CONTROL_MODE_ADDR, 1)) 
      {
        // Error handling
        Serial.println("- Failed to write Control Mode: On/Off! "+ slaveID);
        Serial.println(ModbusRTUClient.lastError());
        return false;
      }
      break;
    case 2:
      if (!ModbusRTUClient.holdingRegisterWrite(slaveID, CONTROL_MODE_ADDR, 2)) 
      {
        // Error handling
        Serial.println("- Failed to write Control Mode: Manual! "+ slaveID);
        Serial.println(ModbusRTUClient.lastError());
        return false;
      }
      break;
    case 3:
      if (!ModbusRTUClient.holdingRegisterWrite(slaveID, CONTROL_MODE_ADDR, 3)) 
      {
        // Error handling
        Serial.println("- Failed to write Control Mode: Ramp/Soak! "+ slaveID);
        Serial.println(ModbusRTUClient.lastError());
        return false;
      }
      break;
  }
};

// Get Control Mode parameter
short getControlMode(int slaveID)
{
  short currentControlMode;
  // Send Reading request over RS485
  if(!ModbusRTUClient.requestFrom(slaveID, HOLDING_REGISTERS, CONTROL_MODE_ADDR, 1))
  {
    // Error handling
    Serial.println("- Failed to request Control Mode! "+ slaveID);
    Serial.println(ModbusRTUClient.lastError());
  }
  else
  {
    // Response handler
    currentControlMode = ModbusRTUClient.read();
  }
  return currentControlMode;
};


// Get current Process Value
float getProcessValue(int slaveID)
{
  float currentProcessValue = 0.0;

  // Send Reading request over RS485
  if(!ModbusRTUClient.requestFrom(slaveID, HOLDING_REGISTERS, PROCESS_VALUE_ADDR, 1))
  {
    // Error handling
    Serial.println("- Failed to request Process Value! "+ slaveID);
    Serial.println(ModbusRTUClient.lastError());
  }
  else
  {
    // Response handler
    currentProcessValue = ModbusRTUClient.read();
  }
  return currentProcessValue;
};


// Set Set Point Value
bool setSetPointValue(int slaveID, float newSetPointValueDegreesC)
{
  // Ensure device is in PID or Ramp/Soak mode
  if((getControlMode(slaveID) == 0) || (getControlMode(slaveID) == 3))
  {
    // Convert from Celcius 
    float newSetPointValue =  newSetPointValueDegreesC;

    // Write new Set Point Value
    if (!ModbusRTUClient.holdingRegisterWrite(slaveID, SET_POINT_VALUE_ADDR, newSetPointValue)) 
    {
      // Error handling
      Serial.println("- Failed to write Set Point Value! "+ slaveID);
      Serial.println(ModbusRTUClient.lastError());
      return false;
    }
    else 
    {
      return true;
    }

  }
  // Error handling
  else if((getControlMode(slaveID)==1)|| getControlMode(slaveID)==2)
  {
    Serial.println("- Control mode not set to PID!"+ slaveID);
    return false;
  }
};


// Get Set Point Value
float getSetPointValue(int slaveID)
{
  float currentSetPointValue = 0.0;
  // Send Reading request over RS485
  if(!ModbusRTUClient.requestFrom(slaveID, HOLDING_REGISTERS, SET_POINT_VALUE_ADDR, 2))
  {
    // Error handling
    Serial.println("- Failed to request Set Point! "+ slaveID);
    Serial.println(ModbusRTUClient.lastError());
  }
  else
  {
    // Response handler
    currentSetPointValue = ModbusRTUClient.read();
  }
  return currentSetPointValue;
};


// Get Auto Tuning parameter state
short getAutoTuningState(int slaveID)
{
  short autoTuningState = 0x00;
  {
  // Send Reading request over RS485
  if(!ModbusRTUClient.requestFrom(slaveID, COILS, AUTO_TUNING_ADDR, 1))
  {
    // Error handling
    Serial.println("- Failed to request Auto Tuning State! "+ slaveID);
    Serial.println(ModbusRTUClient.lastError());
  }
  else
  {
    // Response handler
    autoTuningState = ModbusRTUClient.read();
  }
  return autoTuningState;
  }
};


// Set Auto Tuning parameter
bool setAutoTuning(int slaveID)
{
  // Check if control mode is set to PID mode
  if(getControlMode(slaveID) == 0)
  {
      short autoTuningState = 0x00;
    // Set Auto Tuning Value to 1

    if (!ModbusRTUClient.coilWrite(slaveID, AUTO_TUNING_ADDR, 0x01)) 
    {
      // Error handling
      Serial.println("- Failed to write Set Auto Tuning! "+ slaveID);
      Serial.println(ModbusRTUClient.lastError());
      return false;
    }
    else
    {
      //Wait for auto tuning to complete

      while(autoTuningState == 0) // Check autotuning state
      {
        Serial.println("Auto Tuning..."+ slaveID);
        autoTuningState = getAutoTuningState(1);
        delay(1000);
      }
      Serial.println("-----Auto Tuning Complete-----"+ slaveID);
    }
  }
  // Error handling
  else
  {
    Serial.println("- Control mode not set to PID!"+ slaveID);
    return false;
  }
  return true;
};

// Set Decimal Point Display Selection parameter
bool setDecimalPointDisplaySelectionPid(int slaveID)
{
  // Write new Input Range High Value
    if (!ModbusRTUClient.coilWrite(slaveID, DECIMAL_POINT_DISPLAY_SELECTION_ADDR, 0)) 
    {
      // Error handling
      Serial.println("- Failed to write Decimal Point Display Selection! "+ slaveID);
      Serial.println(ModbusRTUClient.lastError());
      return false;
    }
    else{
      return true;
    }
};


// Get Decimal Point Display Selection parameter
short getDecimalPointDisplaySelectionPid(int slaveID)
{
  short currentDecimalPointDisplaySelection = 0;

  // Send Reading request over RS485
  if(!ModbusRTUClient.requestFrom(slaveID, COILS, DECIMAL_POINT_DISPLAY_SELECTION_ADDR, 1))
  {
    // Error handling
    Serial.println("- Failed to request Decimal Point Display Selection! "+ slaveID);
    Serial.println(ModbusRTUClient.lastError());
  }
  else
  {
    // Response handler
    currentDecimalPointDisplaySelection = ModbusRTUClient.read();
  }
  return currentDecimalPointDisplaySelection;

  
};

// Set input range
bool setInputRange(int slaveID)
{
  // Write Input Range High Value
    if (!ModbusRTUClient.holdingRegisterWrite(slaveID, INPUT_RANGE_HIGH_ADDR, 466.667)) 
    {
      // Error handling
      Serial.println("- Failed to write input range high! "+ slaveID);
      Serial.println(ModbusRTUClient.lastError());
      return false;
    }
    // Set input range low value
    if (!ModbusRTUClient.holdingRegisterWrite(slaveID, INPUT_RANGE_LOW_ADDR, 0)) 
    {
      // Error handling
      Serial.println("- Failed to write input range low! "+ slaveID);
      Serial.println(ModbusRTUClient.lastError());
      return false;
    }
    else{
      return true;
    }
};

// Set PV Offset
bool setPVOffset(int slaveID)
{

  if (!ModbusRTUClient.holdingRegisterWrite(slaveID, PV_OFFSET_ADDR, -17)) 
  {
    // Error handling
    Serial.println("- Failed to write PV offset! "+ slaveID);
    Serial.println(ModbusRTUClient.lastError());
    return false;
  }
  else{
    return true;
  }
};


