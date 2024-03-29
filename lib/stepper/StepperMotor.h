#ifndef StepperMotor_h
#define StepperMotor_h

#include <Arduino.h>

class StepperMotor {
  public:
    StepperMotor(int pin1, int pin2, int pin3, int pin4);
    void oneStep(bool dir);
    void setDirection(bool dir);
    void setRunning(bool running);
    void runIfNeeded();

  private:
    int pins[4];
    int stepNumber;
    bool direction = false; // Standardmäßig Gegen den Uhrzeigersinn
    bool running = false;
};

#endif
