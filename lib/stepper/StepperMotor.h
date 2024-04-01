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
    void moveSteps(int steps); // Zum Bewegen um eine bestimmte Anzahl von Schritten
    void goToInitialPosition(); // Initialisiert den Motor in eine Startposition
    void setStepsPerRevolution(int steps); // Setter für stepsPerRevolution
    int getStepsForDegrees(int degrees);

  private:
    int pins[4];
    int stepNumber;
    bool direction = false; // Standardmäßig Gegen den Uhrzeigersinn
    bool running = false;
    int totalSteps; // Hält die Gesamtzahl der Schritte seit dem letzten Reset
    int stepsPerRevolution; // Schritte pro Umdrehung
};

#endif
