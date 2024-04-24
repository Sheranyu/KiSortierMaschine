#ifndef StepperMotor_h
#define StepperMotor_h

#include <Arduino.h> // Inkludiert die Grundbibliothek für Arduino-Funktionen und -Datentypen.

class StepperMotor {
  public:
    StepperMotor(int pin1, int pin2, int pin3, int pin4); // Konstruktor, nimmt Pins für die Motorsteuerung.
    void oneStep(bool dir); // Führt einen Motor-Schritt aus; 'dir' gibt die Richtung an.
    void setDirection(bool dir); // Setzt die Drehrichtung des Motors.
    void setRunning(bool running); // Startet oder stoppt den Motor.
    void runIfNeeded(); // Führt einen Schritt aus, wenn der Motor aktiv ist.
    void moveSteps(int steps); // Zum Bewegen um eine bestimmte Anzahl von Schritten
    void goToInitialPosition(); // Initialisiert den Motor in eine Startposition
    void setStepsPerRevolution(int steps); // Setter für stepsPerRevolution
    int getStepsForDegrees(int degrees); // Berechnet die Anzahl der Schritte für die gegebenen Grad.
    void goCommandReceived(); // Spezielle Funktion zur Verarbeitung des "go" Befehls.

  private:
    int pins[4]; // Speichert die Pinnummern für die Motorsteuerung.
    int stepNumber; // Speichert den aktuellen Schritt im Zyklus.
    bool direction = false; // Standardmäßig Gegen den Uhrzeigersinn
    bool running = false; // Speichert, ob der Motor läuft oder nicht.
    int totalSteps; // Hält die Gesamtzahl der Schritte seit dem letzten Reset
    int stepsPerRevolution; // Schritte pro Umdrehung
    int goCommandCount = 0; // Zählt, wie oft der "go"-Befehl empfangen wurde.
};

#endif
