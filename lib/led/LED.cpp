#include "LED.h"

LED::LED(int pinR, int pinG, int pinB) {
  pinRed = pinR;
  pinGreen = pinG;
  pinBlue = pinB;
  pinMode(pinRed, OUTPUT);
  pinMode(pinGreen, OUTPUT);
  pinMode(pinBlue, OUTPUT);
}

void LED::setColor(int R, int G, int B) {
  analogWrite(pinRed, R);
  analogWrite(pinGreen, G);
  analogWrite(pinBlue, B);
}
