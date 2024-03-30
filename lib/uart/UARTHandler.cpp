#include "UARTHandler.h"
#include "StepperMotor.h"
#include <Servo.h>

extern Servo servo;
extern StepperMotor stepperMotor; // Definiere dies extern, um Zugriff darauf zu haben

UARTHandler::UARTHandler(LED& led) : ledObj(led), servoControl(nullptr) {
    motorRunning = false;
    incomingCommand = "";
}

void UARTHandler::processInput() {
  if (Serial.available() > 0) {
    // char receivedChar = Serial.read();
    // Serial.print(receivedChar);
    incomingCommand = Serial.readString();
    // Serial.println("Received: " + incomingCommand);
    

    
      if (incomingCommand.startsWith("start")) {
        Serial.println("\nStarte Schrittmotor...");
        stepperMotor.setRunning(true);
      }
      else if (incomingCommand.startsWith("stop")) {
        Serial.println("\nStoppe Schrittmotor...");
        stepperMotor.setRunning(false);
      }
      else if (incomingCommand.startsWith("sg1")) {
        int angle = incomingCommand.substring(3).toInt();
        Serial.println("\nSetze Servoposition...");
        setServoAngle(angle);
      }
      else if (incomingCommand.startsWith("dir")) {
        bool dir = incomingCommand.substring(3) == "1";
        stepperMotor.setDirection(dir);
        Serial.println(dir ? "\nRichtung: im Uhrzeigersinn" : "\nRichtung: gegen den Uhrzeigersinn");
      }
      else if (incomingCommand.startsWith("led")) {
        processLEDCommand(incomingCommand);
        Serial.println("LED umgeschaltet");
      }
      else if (incomingCommand.startsWith("testservo")) {
        if (servoControl != nullptr) {
          servoControl->testServo();
          Serial.println("Testmodus für Servo umgeschaltet.");
        }
      }
      else if (incomingCommand.length() > 0) {
        Serial.println("\nUnknown command: " + incomingCommand);
      }
      incomingCommand = "";
  }
}

void UARTHandler::setMotorRunning(bool running) {
  motorRunning = running;
}

void UARTHandler::processLEDCommand(String command) {
  if (command.startsWith("led")) {
    int R = command.substring(3, 6).toInt();
    int G = command.substring(6, 9).toInt();
    int B = command.substring(9, 12).toInt();
    ledObj.setColor(R, G, B);
    Serial.println("Setze LED auf " + command.substring(3, 12));
  }
}

void UARTHandler::setServoAngle(int angle) {
    if (servoControl != nullptr) {
        servoControl->setAngle(angle);
        Serial.print("Setze Servo-Winkel auf: ");
        Serial.println(angle);
    }
}

void UARTHandler::setServoControl(ServoControl& servoControl) {
    this->servoControl = &servoControl;
}