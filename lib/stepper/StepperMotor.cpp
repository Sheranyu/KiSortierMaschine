#include "StepperMotor.h"

StepperMotor::StepperMotor(int pin1, int pin2, int pin3, int pin4) {
  pins[0] = pin1;
  pins[1] = pin2;
  pins[2] = pin3;
  pins[3] = pin4;
  for (int i = 0; i < 4; i++) {
    pinMode(pins[i], OUTPUT);
  }
  stepNumber = 0;
}

void StepperMotor::setDirection(bool dir) {
  direction = dir;
}

void StepperMotor::oneStep(bool dir) {
  int stepCount = 4;  // Anzahl der Schritte in deiner Sequenz
  digitalWrite(pins[stepNumber % 4], LOW);  // Schalte den aktuellen Pin aus
  if (direction) {
    stepNumber++;
  } else {
    stepNumber--;
  }
  if (stepNumber >= stepCount) {
    stepNumber = 0;
  } else if (stepNumber < 0) {
    stepNumber = stepCount - 1;
  }
  digitalWrite(pins[stepNumber % 4], HIGH);  // Schalte den nächsten Pin ein
}


