#include "MyMotor.h"

Motor::Motor(byte MOTA, byte MOTB)

{
    _MOTA = MOTA;
    _MOTB = MOTB;
}

void Motor::begin()
{
    pinMode(_MOTA, OUTPUT);
    pinMode(_MOTB, OUTPUT);
    ledcAttach(_MOTA, _PWM_FREQ, _PWM_RES);
    ledcAttach(_MOTB, _PWM_FREQ, _PWM_RES);
}

void Motor::send_pwm(double motor_cmd)
{
    if (motor_cmd < 0)
    {
        ledcWrite(_MOTA, 1);
        ledcWrite(_MOTB, abs(motor_cmd));
    }
    else
    {
        ledcWrite(_MOTB, 1);
        ledcWrite(_MOTA, abs(motor_cmd));
    }
}