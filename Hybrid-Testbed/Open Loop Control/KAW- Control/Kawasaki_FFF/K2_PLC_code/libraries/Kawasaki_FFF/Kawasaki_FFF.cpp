/**
 *  Author: Walter W Glockner
 *  Contributer: Jakob D Hamilton
 * 
 *  Description:
 *  This file is the source file for Kawasaki_FFF.h
 * 
 * 
*/


#include <Arduino.h>
#include <Kawasaki_FFF.h>
#include <P1AM.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>
#include <SL4848CR.h>

/////////////////////////////////////////////////////////
//                 Extruder Control                    //
/////////////////////////////////////////////////////////


// Set enable for steppers
bool Extruder::setEnableMotor(float motorSignal, channelLabel extrusionMotorAnalogPin, channelLabel kawGoesMOOvePin){
    P1.writeAnalog(motorSignal, extrusionMotorAnalogPin);
    P1.writeDiscrete(HIGH, kawGoesMOOvePin);
    _enableMotor = true;
    return true;
}

// Get enable for steppers
bool Extruder::getEnableMotor(){
    return _enableMotor;

}

// Set maximum motor Speed
bool Extruder::setMaxMotorSpeed(float maxMotorSpeed){
  _maxMotorSpeed = maxMotorSpeed;
  return true;
}

// Get maximum motor Speed
float Extruder::getMaxMotorSpeed(){
  return _maxMotorSpeed;
}

// Stop extrusion motor
bool Extruder::stopEMotor(channelLabel kawGoesMOOvePin, channelLabel extrusionMotorAnalogPin){
    //setSetPointValue(1,0);
    P1.writeDiscrete(LOW, kawGoesMOOvePin);
    P1.writeAnalog(2048, extrusionMotorAnalogPin);
    

    return true;

}

// Retract extrusion motor
bool Extruder::eMotorRetract(){
    return true;

}

// Set extruder temperature
bool SL4848CR::setTemp(float extruderTemp){
    _extruderTemp = extruderTemp;
    return true;

}

// Get extruder temperature
float SL4848CR::getTemp(){
    return _extruderTemp;

}

// Deretract the extruder motor
bool Extruder::eMotorDeretract(){
    return true;

}

// Set the extruder flow rate 
bool Extruder::setExtrudeFlowrate(float flowrate){
    _flowrate = flowrate;
    return true;

}

// Get the extruder flow rate 
float Extruder::getExtrudeFlowrate(){
    return _flowrate;

}

// True when some extrusion has already taken place
bool Extruder::setWasExtruding(){
    _wasExtruding = true;
    return true;

}

// Returns true when some extrusion has already taken place
bool Extruder::getWasExtruding(){
    return _wasExtruding;

}

// Set extrusion motor speed 
bool Extruder::setMotorSpeed(signed int motorSpeed){
    _motorSpeed = motorSpeed;
    return true;
}

// Get extrusion motor speed
float Extruder::getMotorSpeed(){
  return _motorSpeed;

}


/////////////////////////////////////////////////////////
//                 SL4848-CR Control                   //
/////////////////////////////////////////////////////////

// Initialize parameters for SL4848-CR
bool SL4848CR::init(int slaveID)
{
  // Start Serial Communication
  //while(!Serial);

  // Set Control Mode
  //while(!setControlMode(slaveID,controlMode));

  // Set Input Range to temp transmitter specs
  while(!setInputRange(slaveID));

  // Set PV offset
  while(!setPVOffset(slaveID));
  return true;
};


// Set Control Mode Parameter
bool SL4848CR::setControlMode(int slaveID, int mode)
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
short SL4848CR::getControlMode(int slaveID)
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
float SL4848CR::getProcessValue(int slaveID)
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
bool SL4848CR::setSetPointValue(int slaveID, float newSetPointValueDegreesC)
{
  // Ensure device is in PID or Ramp/Soak mode
  
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
};


// Get Set Point Value
float SL4848CR::getSetPointValue(int slaveID)
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
short SL4848CR::getAutoTuningState(int slaveID)
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
bool SL4848CR::setAutoTuning(int slaveID)
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
bool SL4848CR::setDecimalPointDisplaySelectionPid(int slaveID)
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
short SL4848CR::getDecimalPointDisplaySelectionPid(int slaveID)
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
bool SL4848CR::setInputRange(int slaveID)
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
  bool SL4848CR::setPVOffset(int slaveID)
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

  // Waits for PV = SV to return true
  bool SL4848CR::atTemp(int slaveID){
    float currentProcessValue;
      currentProcessValue = getProcessValue(slaveID);
      if(getProcessValue(slaveID) <= getSetPointValue(slaveID)){
        return false;
      }
      else{
        return true;
      }
      return true;

  };

 

    // retract filiment at retract flowrate

/////////////////////////////////////////////////////////
//               Heated Print Bed Control              //
/////////////////////////////////////////////////////////

// Set bed temperature in degrees C
bool PrintBed::setBedTemp(float bedTemp){
     _bedTemp = bedTemp;
    return true;
}
// Get bed temperature
float PrintBed::getBedTemp(){
    return _bedTemp;
}


/////////////////////////////////////////////////////////
//               Modbus RTU Client Initialize          //
/////////////////////////////////////////////////////////

// Start Modbus RTU Client
bool ModbusClientKAW::init()
{
  // Wait for Serial connection
  //while(!Serial);
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

/////////////////////////////////////////////////////////
//              Send to Kawasaki Controller            //
/////////////////////////////////////////////////////////

bool sendKaw::move(channelLabel kawGoesMOOvePin){
  P1.writeDiscrete(HIGH, kawGoesMOOvePin);
}

bool sendKaw::stop(channelLabel kawGoesMOOvePin){
  P1.writeDiscrete(LOW, kawGoesMOOvePin);
}