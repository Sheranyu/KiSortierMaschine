#include "UARTHandler.h"
#include "StepperMotor.h"
#include <Servo.h>

extern Servo servo; // Globale Referenz auf ein Servo-Objekt
extern StepperMotor stepperMotor; // Globale Referenz auf ein StepperMotor-Objekt

// Konstruktor: Initialisiert den UART-Handler mit einer Referenz auf ein LED-Objekt und setzt Standardwerte.
UARTHandler::UARTHandler(LED& led) : ledObj(led), servoControl(nullptr) {
    motorRunning = false; // Initialisiert den Motorbetriebszustand auf "aus"
    incomingCommand = ""; // Initialisiert die eingehende Befehlszeichenkette
}

// Verarbeitet eingehende Befehle über die serielle Schnittstelle.
void UARTHandler::processInput() {
  if (Serial.available() > 0) { // Prüft, ob Daten über die serielle Verbindung verfügbar sind
    incomingCommand = Serial.readString(); // Liest die gesamte verfügbare Eingabe als Zeichenkette
    incomingCommand.trim(); // Entfernt führende und abschließende Leerzeichen

    // Überprüft auf spezifische Befehle und führt entsprechende Aktionen aus:
    if (incomingCommand.startsWith("start")) {
      Serial.println("\nStarte Schrittmotor..."); // Sendet eine Rückmeldung an den Serial Monitor
      stepperMotor.setRunning(true); // Setzt den Betriebszustand des Motors auf "ein"
    } else if (incomingCommand.startsWith("stop")) {
      Serial.println("\nStoppe Schrittmotor..."); // Sendet eine Rückmeldung
      stepperMotor.setRunning(false); // Setzt den Betriebszustand des Motors auf "aus"
    } else if (incomingCommand.startsWith("sg1")) {
      int angle = incomingCommand.substring(3).toInt(); // Extrahiert den Winkel aus dem Befehl
      Serial.print("Setze Servo auf Winkel: "); // Sendet eine Nachricht
      Serial.println(angle); // Gibt den extrahierten Winkel aus
      setServoAngle(angle); // Stellt den Servo auf den gegebenen Winkel
    } else if (incomingCommand.startsWith("diru")) {
      stepperMotor.setDirection(true); // Ändert die Drehrichtung des Motors auf "vorwärts"
      Serial.println("\nRichtung: im Uhrzeigersinn"); // Sendet eine Rückmeldung
    } else if (incomingCommand.startsWith("dirgu")) {
      stepperMotor.setDirection(false); // Ändert die Drehrichtung des Motors auf "rückwärts"
      Serial.println("\nRichtung: gegen den Uhrzeigersinn"); // Sendet eine Rückmeldung
    } else if (incomingCommand.startsWith("go")) {
      stepperMotor.goCommandReceived(); // Verarbeitet den "go"-Befehl im StepperMotor
    } else if (incomingCommand.startsWith("init")) {
      Serial.println("\nFahre Steppermotor in Initialisierungsposition..."); // Sendet eine Rückmeldung
      stepperMotor.goToInitialPosition(); // Bewegt den Motor in die Startposition
    } else if (incomingCommand.startsWith("b1")) {
      if (servoControl != nullptr) {
        servoControl->moveToCup(1); // Bewegt den Servo zur Position von Becher 1
      }
    } else if (incomingCommand.startsWith("b2")) {
      if (servoControl != nullptr) {
        servoControl->moveToCup(2); // Bewegt den Servo zur Position von Becher 2
      }
    } else if (incomingCommand.startsWith("b3")) {
      if (servoControl != nullptr) {
        servoControl->moveToCup(3); // Bewegt den Servo zur Position von Becher 3
      }
    } else if (incomingCommand.startsWith("b4")) {
      if (servoControl != nullptr) {
        servoControl->moveToCup(4); // Bewegt den Servo zur Position von Becher 4
      }
    } else if (incomingCommand.startsWith("led")) {
      processLEDCommand(incomingCommand); // Verarbeitet LED-bezogene Befehle
    } else if (incomingCommand == "blau" || incomingCommand == "blue" || incomingCommand == "gruen" ||
               incomingCommand == "green" || incomingCommand == "weiss" || incomingCommand == "white" ||
               incomingCommand == "gelb" || incomingCommand == "yellow" || incomingCommand == "rot" ||
               incomingCommand == "red" || incomingCommand == "lila" || incomingCommand == "purple" ||
               incomingCommand == "schwarz" || incomingCommand == "black" || incomingCommand == "sonstig" ||
               incomingCommand == "other") {
      ledObj.setColorByName(incomingCommand); // Setzt die LED-Farbe basierend auf dem Befehlsnamen
    } else if (incomingCommand.startsWith("testservo")) {
      if (servoControl != nullptr) {
        servoControl->testServo(); // Aktiviert den Testmodus für den Servo
        Serial.println("Testmodus für Servo umgeschaltet.");
      }
    } else if (incomingCommand.length() > 0) {
      Serial.println("\nUnknown command: " + incomingCommand); // Gibt eine Fehlermeldung für unbekannte Befehle aus
    }
    incomingCommand = ""; // Setzt die Befehlszeichenkette zurück
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