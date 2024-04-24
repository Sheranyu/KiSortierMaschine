#ifndef ServoControl_h
#define ServoControl_h

#include <Arduino.h> // Inkludiere die Grundbibliothek für Arduino-Funktionen
#include <Servo.h>   // Inkludiere die Bibliothek zur Steuerung von Servomotoren

// Definiert die Klasse ServoControl zur Steuerung eines Servomotors
class ServoControl {
public:
    ServoControl(int pin); // Konstruktor, der den Pin angibt, an dem der Servo angeschlossen ist
    void attach(); // Methode zum Initialisieren des Servos
    void testServo(); // Schaltet den Testmodus um
    void update(); // Aktualisiert den Zustand des Servos, wenn der Testmodus aktiv ist
    void setAngle(int angle); // Setzt den Winkel des Servos
    void moveToCup(int cupNumber); // Bewegt den Servo zu einer vorgegebenen Position basierend auf der Bechernummer

private:
    Servo servo; // Instanz eines Servo-Objekts
    int servoPin; // Pin, an dem der Servo angeschlossen ist
    bool isTesting = false; // Statusvariable, die angibt, ob der Testmodus aktiv ist
    unsigned long lastUpdate; // Zeitstempel der letzten Aktualisierung
    int angle = 0; // Der aktuelle Winkel des Servos
    int direction = 1; // Die Richtung der Servobewegung im Testmodus
};

#endif