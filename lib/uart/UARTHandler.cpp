#include "UARTHandler.h"
#include "StepperMotor.h"
#include <Servo.h>

extern Servo servo;
extern StepperMotor stepperMotor;

// Konstruktor: Initialisiert den UART-Handler mit einer Referenz auf ein LED-Objekt und setzt Standardwerte.
UARTHandler::UARTHandler(LED& led) : ledObj(led), servoControl(nullptr) {
    motorRunning = false; // Initialisiert den Motorbetriebszustand auf "aus"
    incomingCommand = ""; // Initialisiert die eingehende Befehlszeichenkette
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
      else if (incomingCommand == "blau" || incomingCommand == "blue" || incomingCommand == "gruen" ||
            incomingCommand == "green" || incomingCommand == "weiss" || incomingCommand == "white" ||
            incomingCommand == "gelb" || incomingCommand == "yellow" || incomingCommand == "rot" ||
            incomingCommand == "red" || incomingCommand == "lila" || incomingCommand == "purple" ||
            incomingCommand == "schwarz" || incomingCommand == "black" || incomingCommand == "sonstig" ||
            incomingCommand == "other") {
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
  motorRunning = running; // Ändert den Betriebszustand des Motors
}

void UARTHandler::processLEDCommand(String command) {
  if (command.startsWith("led")) {
    int R = command.substring(3, 6).toInt(); // Extrahiert den Rot-Wert
    int G = command.substring(6, 9).toInt(); // Extrahiert den Grün-Wert
    int B = command.substring(9, 12).toInt(); // Extrahiert den Blau-Wert
    Serial.println("Setze LED auf " + command.substring(3, 12)); // Gibt den Farbwert aus
    ledObj.setColor(R, G, B); // Stellt die LED-Farbe ein
  }
}

void UARTHandler::setServoAngle(int angle) {
  if (servoControl != nullptr) { // Stellt sicher, dass das ServoControl-Objekt gesetzt ist
    servoControl->setAngle(angle); // Stellt den Servo-Winkel ein
  }
}

void UARTHandler::setServoControl(ServoControl& servoControl) {
  this->servoControl = &servoControl; // Setzt das ServoControl-Objekt
}