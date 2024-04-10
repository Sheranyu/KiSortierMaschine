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
    incomingCommand.trim();
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
        Serial.print("Setze Servo auf Winkel: ");
        Serial.println(angle);
        setServoAngle(angle);
      }
      else if (incomingCommand.startsWith("diru")) {
        stepperMotor.setDirection(true);
        Serial.println("\nRichtung: im Uhrzeigersinn");
      }
      else if (incomingCommand.startsWith("dirgu")) {
        stepperMotor.setDirection(false);
        Serial.println("\nRichtung: gegen den Uhrzeigersinn");
      }
      else if (incomingCommand.startsWith("go")) {
        stepperMotor.goCommandReceived();
      } 
      else if (incomingCommand.startsWith("init")) {
        Serial.println("\nFahre Steppermotor in Initialisierungsposition...");
        stepperMotor.goToInitialPosition();
      }
      else if (incomingCommand.startsWith("b1")) {
        if (servoControl != nullptr) {
          servoControl->moveToCup(1);
        }
      }
      else if (incomingCommand.startsWith("b2")) {
        if (servoControl != nullptr) {
          servoControl->moveToCup(2);
        }
      }
      else if (incomingCommand.startsWith("b3")) {
        if (servoControl != nullptr) {
          servoControl->moveToCup(3);
        }
      }
      else if (incomingCommand.startsWith("b4")) {
        if (servoControl != nullptr) {
          servoControl->moveToCup(4);
        }
      }
      else if (incomingCommand.startsWith("led")) {
        processLEDCommand(incomingCommand);
      }
      else if (incomingCommand == "blau" || incomingCommand == "rot" || incomingCommand == "gruen" ||
            incomingCommand == "lila" || incomingCommand == "weiss" || incomingCommand == "schwarz" ||
            incomingCommand == "gelb" || incomingCommand == "sonstig") {
            ledObj.setColorByName(incomingCommand);
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
    Serial.println("Setze LED auf " + command.substring(3, 12));
    ledObj.setColor(R, G, B);
  }
}

void UARTHandler::setServoAngle(int angle) {
    if (servoControl != nullptr) {
        servoControl->setAngle(angle);
    }
}

void UARTHandler::setServoControl(ServoControl& servoControl) {
    this->servoControl = &servoControl;
}