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
  Serial.println("led_umgeschaltet");
}

void LED::setColorByName(String colorName) {
    if (colorName == "rot") {
        setColor(255, 0, 0);
    } else if (colorName == "gruen") {
        setColor(0, 255, 0);
    } else if (colorName == "blau") {
        setColor(0, 0, 255);
    } else if (colorName == "lila") {
        setColor(153, 0, 153);
    } else if (colorName == "weiss") {
        setColor(255, 255, 255);
    } else if (colorName == "schwarz") {
        setColor(0, 0, 0);
    } else if (colorName == "gelb") {
        setColor(158, 94, 0);
    } else if (colorName == "sonstig") {
        setColor(0, 255, 255); // Cyan
    } else {
        Serial.println("Unbekannter Farbbefehl: " + colorName);
    }
}
