#include <Arduino.h>
#include <Servo.h>
#include "StepperMotor.h"
#include "UARTHandler.h"
#include "LED.h"
#include "Button.h"

#define STEPPER_PIN_1 PA5
#define STEPPER_PIN_2 PA6
#define STEPPER_PIN_3 PA7
#define STEPPER_PIN_4 PA8

#define SERVO_PIN PB7

#define LED_PIN_RED PC5
#define LED_PIN_GREEN PC6
#define LED_PIN_BLUE PC8

#define BUTTON_PIN PC9


LED led(LED_PIN_RED, LED_PIN_GREEN, LED_PIN_BLUE);

Servo servo; // Globales Servo-Objekt, das im UARTHandler.cpp extern referenziert wird
StepperMotor stepperMotor(STEPPER_PIN_1, STEPPER_PIN_2, STEPPER_PIN_3, STEPPER_PIN_4); // Extern im UARTHandler.cpp
Button button(BUTTON_PIN);
UARTHandler uartHandler(led); // Verwendet servo und stepperMotor

void setup() {
  Serial.begin(9600); // Initialisiere die serielle Kommunikation
  servo.attach(SERVO_PIN); // Binde das Servo-Objekt an den entsprechenden Pin
  button.setMotorControlCallback([](bool pressed) {
    static bool motorRunning = false;
    if (pressed) {
      motorRunning = !motorRunning;
      stepperMotor.setRunning(motorRunning);
    }
  });
}

void loop() {
  uartHandler.processInput(); // Verarbeitet UART-Eingaben
  button.update();
  stepperMotor.runIfNeeded(); // Steuert den Motor basierend auf seinem Zustand
}
