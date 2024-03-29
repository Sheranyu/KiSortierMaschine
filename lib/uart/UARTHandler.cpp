#include "UARTHandler.h"
#include "StepperMotor.h"
#include <Servo.h>

extern Servo servo;
extern StepperMotor stepperMotor; // Definiere dies extern, um Zugriff darauf zu haben

UARTHandler::UARTHandler(LED& led) : ledObj(led) {
  motorRunning = false;
  incomingCommand = "";
  
}

void UARTHandler::processInput() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    Serial.print(receivedChar);
    
    if (receivedChar == ';' || receivedChar == '\n' || receivedChar == '\r') {
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
      }
      else if (incomingCommand.length() > 0) {
        Serial.println("\nUnknown command: " + incomingCommand);
      }
      incomingCommand = "";
    } else {
      incomingCommand += receivedChar;
    }
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
  if (angle >= 0 && angle <= 180) {
    servo.write(angle);
  }
}
