/**

Author: Walter W Glockner
Date:2/3/2024

Contents:

This FIle contains all of the register addresses 
for the SL4848-CR heater.

*/
#ifndef SL4848CR_H
#define SL4848CR_H

#include <Arduino.h>

// Initialize parameters for SL4848-CR
bool SL4848CRInit(int slaveID, int SL4848CR_BAUD_RATE, int controlMode, float inputRangeHigh, float inputRangeLow, signed int PVOffset);

// Start Modbus RTU Client
bool ModbusRTUClientInit(int SL4848_BAUD_RATE);

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

// Set Input Range High Parameter
bool setInputRangeHigh(int slaveID, float inputRangeHigh);

// Set Input Range Low Parameter
bool setInputRangeLow(int slaveID, float inputRangeLow);

// Get Input Range High parameter
float getInputRangeHigh(int slaveID);

// Get Input Range Low parameter
float getInputRangeLow(int slaveID);

// Set Decimal Point Display Selection parameter
bool setDecimalPointDisplaySelection(int slaveID, int type);

// Get Decimal Point Display Selection parameter
short getDecimalPointDisplaySelection(int slaveID);

// Set Present Value Offset parameter
bool setPVOffset(int slaveID, signed int PVOffset);

#endif