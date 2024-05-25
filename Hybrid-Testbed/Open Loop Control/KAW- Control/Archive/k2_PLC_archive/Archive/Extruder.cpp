#include <Arduino.h>
#include <Extruder.h>
#include <P1AM.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>
#include <SL4848CR.h>

    // Set e motor max feedrate
    bool Extruder::setMaxFeedrate(int maxFeedrate){
        _maxFeedrate = maxFeedrate;
        return true;

    }
    // Get e motor max feedrate 
    int Extruder::getMaxFeedrate(){
        return _maxFeedrate;
    }
    // Set acceleration
    bool Extruder::setAcceleration(int accleration){
        _acceleration = accleration;
        return true;
        
    }
    // Get accelleration
    int Extruder::getAcceleration(){
        return _acceleration;

    }
    // Set jerk limits
    bool Extruder::setJerkLimits(int jerkLimits){
        _jerkLimits = jerkLimits;
        return true;

    }
    // Get Jerk limits
    int Extruder::getJerkLimits(){
        return _jerkLimits;

    }
    // Set minimum extruding and travel feedrate
    bool Extruder::setMinExtrudingAndTravelFeedrate(int minExtrudingAndTravelFeedrate){
        _minExtrudingAndTravelFeedrate = minExtrudingAndTravelFeedrate;
        return true;

    }
    // Get minimum extruding and travel feedrate
    int Extruder::getMinExtrudingAndTravelFeedrate(){
        return _minExtrudingAndTravelFeedrate;

    }
    // Set enable for steppers
    bool Extruder::setEnableSteppers(int enableSteppers){
        _enableSteppers = enableSteppers;
        return true;

    }
    // Get enable for steppers
    bool Extruder::getEnableSteppers(){
        return _enableSteppers;

    }
    // Set bed temperature in degrees C
    bool Extruder::setBedTemp(int bedTemp){
        _bedTemp = bedTemp;
        return true;

    }
    // Get bed temperature
    int Extruder::getBedTemp(){
        return _bedTemp;

    }
    // Set extrusion motor bed leveling tempurature
    bool Extruder::setEMotorBedLevelTemp(int eMotorBedLevelTemp){
        _eMotorBedLevelTemp = eMotorBedLevelTemp;
        return true;

    }
    // Get extrusion motor bed level temperature
    int Extruder::getEMotorBedLevelTemp(){
        return _eMotorBedLevelTemp;

    }
    // Stop extrusion motor
    bool Extruder::stopEMotor(){
        return true;

    }
    // Home all without mesh bed leveling
    bool Extruder::homeAllNoMesh(){
        return true;

    }
    // Clean nozzle by probing
    bool Extruder::cleanNozzle(){
        return true;

    }
    // Retract extrusion motor
    bool Extruder::eMotorRetract(){
        return true;

    }
    // Mesh bed level
    bool Extruder::meshBedLevel(){
        return true;

    }
    // Set extruder temperature
    bool Extruder::setExtruderTemp(int extruderTemp){
        _extruderTemp = extruderTemp;
        return true;

    }
    // Get extruder temperature
    int Extruder::getExtruderTemp(){
        return _extruderTemp;

    }
    // Set e motor spread cycle mode
    bool Extruder::setEMotorSpreadcycleMode(){
        return true;

    }
    // Extrude a purge line at the start of the print
    bool Extruder::extrudePurgeLine(){
        return true;

    }
    // Deretract the extruder motor
    bool Extruder::eMotorDeretract(){
        return true;

    }
    // Move the extruder to the start position
    bool Extruder::moveToStartPosition(){
        return true;

    }
    // Set the extruder flow rate 
    bool Extruder::setFlowrate(int flowrate){
        _flowrate = flowrate;
        return true;

    }

    // Get the extruder flow rate 
    int Extruder::getFlowrate(){
        return _flowrate;
    
    }
    // Set the units to be used
    bool Extruder::setUnits(char units){
        _units = units;
        return true;

    }
    // Get the units being used
    int Extruder::getUnits(){

};
