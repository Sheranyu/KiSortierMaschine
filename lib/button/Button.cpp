#include "Button.h"

Button::Button(int pin) : buttonPin(pin), lastButtonState(LOW), currentButtonState(LOW), lastDebounceTime(0), debounceDelay(50), motorControlCallback(nullptr) {
  pinMode(buttonPin, INPUT_PULLUP); // Setzt den Button-Pin als Input mit Pull-Up-Widerstand
}

void Button::update() {
  bool reading = digitalRead(buttonPin);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != currentButtonState) {
      currentButtonState = reading;
      if (currentButtonState == LOW) { // Button wurde gedrückt
        if (motorControlCallback != nullptr) {
          motorControlCallback(!currentButtonState);
        }
      }
    }
  }
  lastButtonState = reading;
}

void Button::setMotorControlCallback(void (*callback)(bool)) {
  motorControlCallback = callback;
}
