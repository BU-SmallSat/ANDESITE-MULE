#include "MC33926_Arduino_FAST_PWM.h"
#define MAX_DUTY_CYCLE 255

//****************************************************//
//********************Constructor*********************//
//****************************************************//
MC33926_Arduino_FAST_PWM::MC33926_Arduino_FAST_PWM(int D1, int INV, int FB, int notSF, int EN)
{
  _D1 = D1;
  _INV = INV;
  _FB = FB;
  _notSF = notSF;
  _EN = EN;
}

//****************************************************//
//******************Member Functions******************//
//****************************************************//
void MC33926_Arduino_FAST_PWM::init()
{
  pinMode(_D1,OUTPUT);
  TCCR2B = (TCCR2B & 0xF8) | 1;

  pinMode(_INV,OUTPUT);
  pinMode(_FB,INPUT);
  pinMode(_notSF,INPUT);
  pinMode(_EN,OUTPUT);
  digitalWrite(_D1,LOW);
  digitalWrite(_EN,HIGH);
  MAX_SPEED = 100;
}
// Set speed for motor 1, speed is a number betwenn -400 and 400
void MC33926_Arduino_FAST_PWM::setSpeed(int speed)
{
  int inverse = 0;
  if (speed < 0)
  {
    speed = -speed;  // Make speed a positive quantity
    inverse = 1;  // Preserve the direction
  }
  
  if (speed > MAX_SPEED)  // Max PWM dutycycle
  speed = MAX_SPEED;
  
  speed = MAX_SPEED - speed;
  double test = ((double)speed/(double)MAX_SPEED)*(double)MAX_DUTY_CYCLE;
  // Serial.println(test); // Commented out on 02/07/2017
  analogWrite(_D1,test); // default to using analogWrite, mapping 100 to 255
  
  if (inverse)
    digitalWrite(_INV,HIGH);
  else
    digitalWrite(_INV,LOW);
}

// Return motor 1 current value in milliamps.
unsigned int MC33926_Arduino_FAST_PWM::getCurrent()
{
  // 5V / 1024 ADC counts / 525 mV per A = 9 mA per count
  return analogRead(_FB) * 9;
}

// Return error status
unsigned char MC33926_Arduino_FAST_PWM::getStatusFlag()
{
  return !digitalRead(_notSF);
}