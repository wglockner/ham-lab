/*
 * Title: WriteDigitalOutput
 *
 * Objective:
 *    This example demonstrates how to write the state of a ClearCore digital
 *    output.
 *
 * Description:
 *    This example repeatedly toggles the state of the ClearCore's six digital
 *    outputs, IO-0 through IO-5.
 *
 * Requirements:
 * ** A device that takes in a digital signal connected to any of the I/O's,
 *    IO-0 through IO-5.
 *      Note: You can leave the I/O points disconnected and still see the
 *      built-in I/O LEDs toggle with the connector state.
 *
 * Links:
 * ** ClearCore Documentation: https://teknic-inc.github.io/ClearCore-library/
 * ** ClearCore Manual: https://www.teknic.com/files/downloads/clearcore_user_manual.pdf
 *
 * Last Modified: 1/21/2020
 * Copyright (c) 2020 Teknic Inc. This work is free to use, copy and distribute under the terms of
 * the standard MIT permissive software license which can be found at https://opensource.org/licenses/MIT
 */

#include "ClearCore.h"
#define motor ConnectorM0
#define baudRate 9600

int velLimit = 10000;
int accLimit = 100000;

float maxRPM = 840;
float velocity;

bool enabled = false;

float speedRef0;
float speedRPM0;

// Declares a variable used to write new states to the output. We will toggle
// this true/false.


void setup() {
    Serial.begin(baudRate);

    analogReadResolution(12);
    //Serial.println("ADC Resolution Set");

    pinMode(DI6, INPUT);

    // Sets the input clocking rate.
    MotorMgr.MotorInputClocking(MotorManager::CLOCK_RATE_NORMAL);

    // Sets all motor connectors into step and direction mode.
    MotorMgr.MotorModeSet(MotorManager::MOTOR_ALL,
                          Connector::CPM_MODE_STEP_AND_DIR);

    // Sets the maximum velocity for each move
    motor.VelMax(velLimit);

    // Set the maximum acceleration for each move
    motor.AccelMax(accLimit);

    motor.EnableRequest(true);

    uint32_t timeout = 5000;
    uint32_t startTime = millis();
    
    
    // Waits for HLFB to assert. Uncomment these lines if your motor has a 
    // "servo on" feature and it is wired to the HLFB line on the connector.
    //Serial.println("Waiting for HLFB...");
    //while (motor.HlfbState() != MotorDriver::HLFB_ASSERTED) {
    //    continue;
    //}
    //Serial.println("Motor Ready");
}

void loop() {
    speedRef0 = (analogRead(A9)/2048.0);
    Serial.print("The analog signal is ");
    Serial.println(analogRead(A9));

    /*
    if (digitalRead(DI6)){
        Serial.println("Motor was enabled");
        //motor.EnableRequest(true);
        enabled = true;
        speedRPM0 = maxRPM*(speedRef0-1.0); // converting to an RPM
        delay(2000);
    } else{
        Serial.println("Motor not enabled");
        //motor.EnableRequest(false);
        enabled = false;
        speedRPM0 = 0; // converting to an RPM
        delay(2000);
    }
    */

    speedRPM0 = (maxRPM*(speedRef0-1.0));
    velocity = speedRPM0;

    motor.MoveVelocity(velocity*14);

    Serial.print("The A9 signal RPM is ");
    Serial.print(speedRPM0);
    Serial.print("           ");
    Serial.println(velocity);
    delay(1000);
}

//------------------------------------------------------------------------------
