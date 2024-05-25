/**

Author: Walter W Glockner
Contributer: Jakob D Hamilton

Date:2/28/2024

Contents:

This FIle contains classes for:

- SL4848CR PID heater
- Clearpath extrusion motor
- Heated printbed
- kawasaki motion control 
- Modbus init

Classes may be added and removed as compnents are
added and removed.  

*/


#ifndef Kawasaki_FFF_h
#define Kawasaki_FFF_h
#include <Arduino.h>
#include <P1AM.h>

//channelLabel extrusionMotorEnablePin = { 4, 9 };
//channelLabel extrusionMotorAnalogPin = { 7, 1 };
//channelLabel kawstart = { 3, 1 };
//channelLabel kawRunPin = { 2, 9 };
//channelLabel ESTOP_PIN = { 1, 1 };


// Data Collection
// making use of constant vecor to have dynamic memory size, 
// functions, and methods.
// 


class Extruder {
public:

    // Set enable for motor
    bool setEnableMotor(float motorSignal, channelLabel extrusionMotorAnalogPin, channelLabel kawGoesMOOvePin);

    // Get enable for motor
    bool getEnableMotor();

    // Set maximum motor Speed
    bool setMaxMotorSpeed(float maxMotorSpeed);

    // Get maximum motor Speed
    float getMaxMotorSpeed();

    // Stop extrusion motor
    bool stopEMotor(channelLabel KawGoesMOOvePin, channelLabel extrusionMotorAnalogPin);

    // Retract extrusion motor
    bool eMotorRetract(); 

    // Deretract the extruder motor
    bool eMotorDeretract();

    // Set the extruder flow rate 
    bool setExtrudeFlowrate(float flowrate);

    // Get the extruder flow rate 
    float getExtrudeFlowrate();

    // Set the extruder flow rate 
    bool setRetractFlowrate(signed int flowrate);

    // Get the extruder flow rate 
    float getRetractFlowrate();

    // Retract filiment at retract flowrate
    bool retract();

    // set true when some extrusion has already taken place
    bool setWasExtruding();

    // return true when extrusion has taken place.
    bool getWasExtruding();

    // Set extrusion motor speed 
    bool setMotorSpeed(signed int motorSpeed);

    // Get extrusion motor speed
    float getMotorSpeed();



private:
   float _motorSignal;
    float _motorSpeed;
    float _maxMotorSpeed;
    int _motorPos;
    float _maxSpeed;
    float _maxFeedrate;
    int _acceleration;
    int _jerkLimits;
    int _minExtrudingAndTravelFeedrate;
    bool _enableMotor;
    float _eMotorBedLevelTemp;
    float  _flowrate;
    char _units;
    bool _wasExtruding;
};

//information to send to kaw
class sendKaw {
public:

    bool move(channelLabel kawGoesMOOvePin);
    bool stop(channelLabel kawGoesMOOvePin);

};

class ModbusClientKAW {
public:

    bool init();

};

class PrintBed {
public:
    // Set bed temperature in degrees C
    bool setBedTemp(float bedTemp);
    // Get bed temperature
    float getBedTemp();
private:
    float _bedTemp;
};

class SL4848CR {
public:

// Initialize parameters for SL4848-CR
bool init(int slaveID);

// Set Control Mode Parameter
bool setControlMode(int slaveID, int mode);

// Get Control Mode parameter
short getControlMode(int slaveID);

// Get current Process Value
float getProcessValue(int slaveID);

// Set Set Point Value
bool setSetPointValue(int slaveID, float newSetPointValueDegreesC);

// Get Set Point Value
float getSetPointValue(int slaveID);

// Get Auto Tuning parameter state
short getAutoTuningState(int slaveID);

// Set Auto Tuning parameter
bool setAutoTuning(int slaveID);

// Set Decimal Point Display Selection parameter
bool setDecimalPointDisplaySelectionPid(int slaveID);

// Get Decimal Point Display Selection parameter
short getDecimalPointDisplaySelectionPid(int slaveID);

// Set input range high and low to 466.667 and 0
bool setInputRange(int slaveID);

// Set Present Value Offset parameter
bool setPVOffset(int slaveID);

// Waits for PV = SV to return true
bool atTemp(int slaveID);

// Set extruder temperature
bool setTemp(float extruderTemp);

// Get extruder temperature
float getTemp();



private:

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
float _currentProcessValue;
float _extruderTemp;

};

#endif