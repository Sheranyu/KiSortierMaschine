#include <Arduino.h>
#include <Servo.h>
#include "StepperMotor.h"
#include "UARTHandler.h"

#define STEPPER_PIN_1 PA5
#define STEPPER_PIN_2 PA6
#define STEPPER_PIN_3 PA7
#define STEPPER_PIN_4 PA8

#define SERVO_PIN PB7

Servo servo; // Globales Servo-Objekt, das im UARTHandler.cpp extern referenziert wird
StepperMotor stepperMotor(STEPPER_PIN_1, STEPPER_PIN_2, STEPPER_PIN_3, STEPPER_PIN_4); // Extern im UARTHandler.cpp
UARTHandler uartHandler; // Verwendet servo und stepperMotor

void setup() {
  Serial.begin(9600); // Initialisiere die serielle Kommunikation
  servo.attach(SERVO_PIN); // Binde das Servo-Objekt an den entsprechenden Pin
}

void loop() {
  uartHandler.processInput(); // Verarbeitet UART-Eingaben

  // Prüfen, ob der Motor laufen soll
  if (uartHandler.isMotorRunning()) {
    // Führt einen Schritt aus, wenn der Motor laufen soll
    // Die Richtung ist bereits im StepperMotor-Objekt eingestellt
    stepperMotor.oneStep(true); // Das 'true' hier ist eigentlich irrelevant, da die Richtung intern im StepperMotor gesteuert wird
    delay(10); // Verzögerung zur Steuerung der Schrittmotorgeschwindigkeit, kann angepasst werden
  }
}
