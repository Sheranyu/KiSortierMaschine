#ifndef ServoControl_h
#define ServoControl_h

#include <Arduino.h>
#include <Servo.h>

class ServoControl {
public:
    ServoControl(int pin);
    void attach();
    void testServo();
    void update();
    void setAngle(int angle);
    void moveToCup(int cupNumber);

private:
    Servo servo;
    int servoPin;
    bool isTesting = false;
    unsigned long lastUpdate;
    int angle = 0;
    int direction = 1;
};

#endif
