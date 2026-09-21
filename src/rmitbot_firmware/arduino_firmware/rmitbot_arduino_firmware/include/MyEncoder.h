#ifndef MY_ENCODER_H // Standard guard while writing a library to prevent multiple inclusions of this header file
#define MY_ENCODER_H

#include <Arduino.h>      // Arduino library for basic functions
#include <ESP32Encoder.h> // ESP32Encoder library for handling encoders

// ==============================================
// Pin definitions for the encoders
// ==============================================
#define ENC1_A 36 // Pin used on ESP32 for the ENC1_A
#define ENC1_B 39 // Pin used on ESP32 for the ENC1_B
#define ENC2_A 35 // Pin used on ESP32 for the ENC2_A
#define ENC2_B 32 // Pin used on ESP32 for the ENC2_B
#define ENC3_A 14 // Pin used on ESP32 for the ENC3_A
#define ENC3_B 13 // Pin used on ESP32 for the ENC3_B
#define ENC4_A 16 // Pin used on ESP32 for the ENC4_A
#define ENC4_B  4 // Pin used on ESP32 for the ENC4_B

inline volatile long EncoderTick1, EncoderTick2, EncoderTick3, EncoderTick4;    // Encoder tick count for encoder 1

inline double w1, w2, w3, w4;   // Speed, reference ,and command for the motor 1

class Encoder
{
public:
    Encoder(byte ENCA, byte ENCB); // Constructor for the Encoder class
    void begin();                  // Method to set the pin mode and enable the encoder
    long getCount();               // Method to read the encoder value
    double getVelocity();          // Method to get the velocity of the encoder

private:
    byte _ENCA, _ENCB;                    // Pin used on ESP32 for the ENC_A and ENC_B
    int _ENC_RES = 330;                   // Encoder resolution
    unsigned long w_time;                 // Time variable used to calculate the velocity
    double th, th_prev, w, w_prev, w_raw; // Variables used to calculate the velocity
    double alpha = .95;                   // Filter coefficient
    ESP32Encoder _encoder;                // ESP32Encoder object to handle the encoder
};

#endif
