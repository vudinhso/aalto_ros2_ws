#ifndef MY_MOTOR_H // Include guard to prevent multiple inclusions of this header file
#define MY_MOTOR_H

#include <Arduino.h>

#define MOT1_A 33 // Pin used on ESP32 for the MOT1_A
#define MOT1_B 25 // Pin used on ESP32 for the MOT1_B
#define MOT2_A 19 // Pin used on ESP32 for the MOT2_A
#define MOT2_B 21 // Pin used on ESP32 for the MOT2_B
#define MOT3_A 27 // Pin used on ESP32 for the MOT3_A
#define MOT3_B 26 // Pin used on ESP32 for the MOT3_B
#define MOT4_A 18 // Pin used on ESP32 for the MOT4_A
#define MOT4_B 17 // Pin used on ESP32 for the MOT4_B

class Motor
{
public:
    Motor(byte MOTA, byte MOTB);       // Constructor to initialize the motor object
    void begin();                    // Method to set the pin mode and enable the motors
    void send_pwm(double motor_cmd); // Method to send the PWM signal to the motors

private:
    byte _MOTA, _MOTB;     // Pin used on ESP32 for the MOT_A
    int _PWM_FREQ = 12000; // Frequency of the PWM signal
    int _PWM_RES = 12;      // Resolution of the PWM signal
};

#endif