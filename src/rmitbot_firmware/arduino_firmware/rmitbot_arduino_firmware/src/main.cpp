#include <Arduino.h> // Arduino library for basic functions

#include "MySetup.h"      // Pin and variable definitions
#include "MyEncoder.h"    // Library for the encoder
#include "MyMotor.h"      // Library for the motor
#include "MyController.h" // Library for the controller
#include "MyIMU.h"        // Library for the IMU
#include "MySerial.h"     // Library for the controller

Encoder encoder1(ENC1_A, ENC1_B);                // Create an instance of the Encoder class
Encoder encoder2(ENC2_A, ENC2_B);                // Create an instance of the Encoder class
Encoder encoder3(ENC3_A, ENC3_B);                // Create an instance of the Encoder class
Encoder encoder4(ENC4_A, ENC4_B);                // Create an instance of the Encoder class
Motor motor1(MOT1_A, MOT1_B);    // Create an instance of the Motor class
Motor motor2(MOT2_A, MOT2_B);    // Create an instance of the Motor class
Motor motor3(MOT3_A, MOT3_B);    // Create an instance of the Motor class
Motor motor4(MOT4_A, MOT4_B);    // Create an instance of the Motor class
Controller controller1(&w1, &MOT1_cmd, &w1_ref); // Create an instance of the Controller class
Controller controller2(&w2, &MOT2_cmd, &w2_ref); // Create an instance of the Controller class
Controller controller3(&w3, &MOT3_cmd, &w3_ref); // Create an instance of the Controller class
Controller controller4(&w4, &MOT4_cmd, &w4_ref); // Create an instance of the Controller class

void setup()
{
  SerialBegin();
  encoder1.begin();    // Initialize the encoder
  encoder2.begin();    // Initialize the encoder
  encoder3.begin();    // Initialize the encoder
  encoder4.begin();    // Initialize the encoder
  motor1.begin();      // Initialize the motor
  motor2.begin();      // Initialize the motor
  motor3.begin();      // Initialize the motor
  motor4.begin();      // Initialize the motor
  controller1.begin(); // Initialize the controller
  controller2.begin(); // Initialize the controller
  controller3.begin(); // Initialize the controller
  controller4.begin(); // Initialize the controller
  IMUBegin();          // Initialize the IMU
}

void loop()
{
  w1 = encoder1.getVelocity(); // Get the velocity from the encoder
  w2 = encoder2.getVelocity(); // Get the velocity from the encoder
  w3 = encoder3.getVelocity(); // Get the velocity from the encoder
  w4 = encoder4.getVelocity(); // Get the velocity from the encoder
  controller1.compute();       // Compute the PID control output
  controller2.compute();       // Compute the PID control output
  controller3.compute();       // Compute the PID control output
  controller4.compute();       // Compute the PID control output
  motor1.send_pwm(MOT1_cmd);   // Send the PWM command to the motor
  motor2.send_pwm(MOT2_cmd);   // Send the PWM command to the motor
  motor3.send_pwm(MOT3_cmd);   // Send the PWM command to the motor
  motor4.send_pwm(MOT4_cmd);   // Send the PWM command to the motor
  IMUGetData();                // Get the data from the IMU
  SerialDataPrint();           // Print the data to the Serial Monitor
  SerialDataRead();            // Write the data to the Serial Monitor
}
