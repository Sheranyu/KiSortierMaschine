#ifndef LED_h
#define LED_h

#include <Arduino.h>

class LED {
public:
  LED(int pinR, int pinG, int pinB);
  void setColor(int R, int G, int B);
  void setColorByName(String colorName);

private:
  int pinRed, pinGreen, pinBlue;
};

#endif
