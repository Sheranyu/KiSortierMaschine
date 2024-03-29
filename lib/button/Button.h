#ifndef Button_h
#define Button_h

#include <Arduino.h>

class Button {
public:
    Button(int pin);
    void update();
    void setMotorControlCallback(void (*callback)(bool));

private:
    int buttonPin;
    bool lastButtonState;
    bool currentButtonState;
    unsigned long lastDebounceTime;
    unsigned long debounceDelay;
    void (*motorControlCallback)(bool);
};

#endif
