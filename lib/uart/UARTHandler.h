#ifndef UARTHandler_h
#define UARTHandler_h

#include <Arduino.h> // Einbinden der Arduino-Standardbibliothek für Zugriff auf Basisfunktionen und -definitionen
#include "LED.h" // Einbinden der LED-Klasse zur Steuerung von LEDs
#include "ServoControl.h" // Einbinden der ServoControl-Klasse zur Steuerung des Servo-Motors

class UARTHandler {
public:
  UARTHandler(LED& led); // Konstruktor, der eine Referenz auf ein LED-Objekt erhält
  void processInput(); // Funktion zum Verarbeiten eingehender Befehle über UART
  void setMotorRunning(bool running); // Funktion zum Steuern des Betriebszustandes des Motors
  void setServoAngle(int angle); // Funktion zum Einstellen des Winkels eines Servo-Motors
  bool isMotorRunning() const; // Funktion zum Abfragen des aktuellen Betriebszustandes des Motors
  void changeMotorDirection(bool dir); // Funktion zum Ändern der Drehrichtung des Motors
  void processLEDCommand(String command); // Funktion zum Verarbeiten spezieller LED-Befehle
  void setServoControl(ServoControl& servoControl); // Funktion zum Setzen des ServoControl-Objekts

private:
  String incomingCommand; // Variable zum Speichern des zuletzt empfangenen Befehls
  bool motorRunning; // Variable zum Speichern des Betriebszustandes des Motors
  LED& ledObj; // Referenz auf das verwendete LED-Objekt
  ServoControl* servoControl; // Zeiger auf das verwendete ServoControl-Objekt
};

#endif