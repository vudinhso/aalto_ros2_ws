#include "MySerial.h"

extern double w1, w1_ref, MOT1_cmd; // Reference and command for the motor 1 - defined in MySetup.h
extern double w2, w2_ref, MOT2_cmd; // Reference and command for the motor 2 - defined in MySetup.h
extern double w3, w3_ref, MOT3_cmd; // Reference and command for the motor 1 - defined in MySetup.h
extern double w4, w4_ref, MOT4_cmd; // Reference and command for the motor 2 - defined in MySetup.h
extern volatile long EncoderTick1;  // Encoder tick count for encoder 1 - defined in MySetup.h
extern volatile long EncoderTick2;  // Encoder tick count for encoder 2 - defined in MySetup.h
extern volatile long EncoderTick3;  // Encoder tick count for encoder 1 - defined in MySetup.h
extern volatile long EncoderTick4;  // Encoder tick count for encoder 2 - defined in MySetup.h
extern double quat[4];          // Quaternion data from the IMU - defined in MySetup.h
extern double gyr[3];           // Gyroscope data from the IMU - defined in MySetup.h
extern double acc[3];           // Accelerometer data from the IMU - defined in MySetup.h
extern unsigned long Serial_time;   // Time for serial communication - defined in MySetup.h
String incomingMessage = "";
bool receiving = false;

void SerialBegin() // Function to initialize the serial communication
{
    Serial.begin(115200);
    while (!Serial)
        ;
}

void SerialDataPrint() // Function to print the data to the Serial Monitor
{
    if (micros() - Serial_time >= 50 * 1e3)
    {
        Serial_time = micros();
        Serial.print('<');
        Serial.print(w1); Serial.print("\t");
        Serial.print(w2); Serial.print("\t");
        Serial.print(w3); Serial.print("\t");
        Serial.print(w4); Serial.print("\t");
        Serial.print(quat[0]); Serial.print("\t");
        Serial.print(quat[1]); Serial.print("\t");
        Serial.print(quat[2]); Serial.print("\t");
        Serial.print(quat[3]); Serial.print("\t");

        Serial.print(gyr[0]); Serial.print("\t");
        Serial.print(gyr[1]); Serial.print("\t");
        Serial.print(gyr[2]); Serial.print("\t");

        Serial.print(acc[0]); Serial.print("\t");
        Serial.print(acc[1]); Serial.print("\t");
        Serial.print(acc[2]); Serial.println(">");
    }
}

void SerialDataRead()
{
    while (Serial.available() > 0)
    {
        char c = Serial.read();

        if (c == '<')
        {
            receiving = true;
            incomingMessage = ""; // Reset buffer
        }
        else if (c == '>')
        {
            receiving = false;
            parseCommand(incomingMessage);
        }
        else if (receiving)
        {
            incomingMessage += c;
        }
    }
}


void parseCommand(const String &msg)
{
  // find the three tab positions
  int t1 = msg.indexOf('\t');
  int t2 = msg.indexOf('\t', t1 + 1);
  int t3 = msg.indexOf('\t', t2 + 1);
 
  // only proceed if all three tabs were found
  if (t1 > 0 && t2 > t1 && t3 > t2)
  {
    // extract each substring between tabs (and after last tab)
    String s1 = msg.substring(0,    t1);
    String s2 = msg.substring(t1+1, t2);
    String s3 = msg.substring(t2+1, t3);
    String s4 = msg.substring(t3+1);
 
    // convert to floats
    w1_ref = s1.toFloat();
    w2_ref = s2.toFloat();
    w3_ref = s3.toFloat();
    w4_ref = s4.toFloat();
  }
  else
  {
    // malformed message—handle error or ignore
    Serial.println("parseCommand: expected 4 tab-separated values");
  }
}


