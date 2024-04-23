// Einbinden der erforderlichen Bibliotheken und Header-Dateien für die Steuerung von Hardwarekomponenten.
#include <Arduino.h>
#include <Servo.h>
#include "StepperMotor.h"
#include "UARTHandler.h"
#include "LED.h"
#include "Button.h"
#include "ServoControl.h"

// Definieren der seriellen Baudrate für die Kommunikation über den Serial Monitor.
#define SERIAL_BAUDRATE 115200

// Pin-Definitionen für die Ansteuerung des Schrittmotors.
#define STEPPER_PIN_1 PA5
#define STEPPER_PIN_2 PA6
#define STEPPER_PIN_3 PA7
#define STEPPER_PIN_4 PA8
#define STEPPER_STEPS_PER_REVOLUTION 2048  // Anzahl der Schritte pro Umdrehung für den 28BYJ-48 Motor.

// Pin-Definition für den Servo-Motor.
#define SERVO_PIN PB7
#define SERVO_INIT 120  // Startposition des Servos in Grad.

// Pin-Definitionen für die RGB-LED.
#define LED_PIN_RED PC5
#define LED_PIN_GREEN PC6
#define LED_PIN_BLUE PC8

// Pin-Definition für den Button.
#define BUTTON_PIN PC9

// Objekte für die Steuerung von LEDs, Servo, Stepper Motor und Buttons.
LED led(LED_PIN_RED, LED_PIN_GREEN, LED_PIN_BLUE);
Servo servo;  // Globales Servo-Objekt.
StepperMotor stepperMotor(STEPPER_PIN_1, STEPPER_PIN_2, STEPPER_PIN_3, STEPPER_PIN_4);
Button button(BUTTON_PIN);
UARTHandler uartHandler(led);  // UARTHandler-Instanz, die die LED-Instanz nutzt.
ServoControl servoControl(SERVO_PIN);  // ServoControl-Instanz für den Servo-Motor.

void setup() {
  Serial.begin(SERIAL_BAUDRATE);  // Initialisiert die serielle Kommunikation mit der festgelegten Baudrate.
  servoControl.attach();  // Initialisiert die Verbindung des Servos mit dem festgelegten Pin.
  uartHandler.setServoControl(servoControl);  // Verknüpft das ServoControl-Objekt mit dem UARTHandler.
  stepperMotor.setStepsPerRevolution(STEPPER_STEPS_PER_REVOLUTION);  // Konfiguriert die Schrittzahl pro Umdrehung für den StepperMotor.
  button.setMotorControlCallback([](bool pressed) {  // Lambda-Funktion, die als Callback für Button-Press-Events dient.
    static bool motorRunning = false;  // Statische Variable zur Speicherung des Laufzustandes des Motors.
    if (pressed) {  // Wenn der Button gedrückt wird.
      motorRunning = !motorRunning;  // Umschalten des Laufzustandes des Motors.
      stepperMotor.setRunning(motorRunning);  // Setzt den Laufzustand des Stepper Motors entsprechend.
      servoControl.testServo();  // Führt eine Testbewegung des Servos aus.
    }
  });
  servoControl.setAngle(SERVO_INIT);  // Setzt den Winkel des Servos auf die Startposition.
}

void loop() {
  uartHandler.processInput();  // Liest und verarbeitet eingehende UART-Befehle.
  servoControl.update();  // Aktualisiert den Zustand des Servos, falls erforderlich.
  button.update();  // Prüft den Zustand des Buttons und führt gegebenenfalls den Callback aus.
  stepperMotor.runIfNeeded();  // Führt einen Schritt des Steppermotors aus, falls dies notwendig ist.
}