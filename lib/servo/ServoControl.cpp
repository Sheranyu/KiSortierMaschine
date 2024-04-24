#include "ServoControl.h"

// Konstruktor: Initialisiert den Servo an einem spezifischen Pin.
ServoControl::ServoControl(int pin) : servoPin(pin), lastUpdate(0) {}

// Befestigt den Servo an dem definierten Pin.
void ServoControl::attach() {
    servo.attach(servoPin);
}

// Umschaltet den Testmodus des Servos.
void ServoControl::testServo() {
    isTesting = !isTesting; // Wechselt den Zustand zwischen aktiv und inaktiv.
}

// Aktualisiert den Servo im Testmodus alle 15 Millisekunden.
void ServoControl::update() {
    if (isTesting) { // Nur im Testmodus ausführen
        unsigned long currentMillis = millis(); // Aktuelle Zeit in Millisekunden
        if (currentMillis - lastUpdate > 15) { // Prüft, ob 15ms seit der letzten Aktualisierung vergangen sind
            lastUpdate = currentMillis;
            angle += direction; // Aktualisiert den Winkel basierend auf der Richtung
            if (angle >= 180 || angle <= 0) { // Prüft, ob die Grenzen erreicht sind
                direction = -direction; // Kehrt die Richtung um
                angle += direction; // Korrigiert den Winkel, um innerhalb der Grenzen zu bleiben
            }
            servo.write(angle); // Schreibt den neuen Winkel an den Servo
        }
    }
}

// Setzt den Servowinkel direkt.
void ServoControl::setAngle(int angle) {
    if (angle >= 0 && angle <= 180) {
        this->angle = angle; // Speichert den neuen Winkel
        servo.write(angle); // Setzt den Winkel am Servo
    }
    Serial.println("servo_gedreht"); // Gibt eine Nachricht aus, dass der Servo gedreht wurde
}

// Bewegt den Servo zu einer spezifischen Position basierend auf der Bechernummer.
void ServoControl::moveToCup(int cupNumber) {
    int angle; // Lokale Variable für den Winkel
    switch (cupNumber) { // Wählt den Winkel basierend auf der Bechernummer
        case 1: angle = 180; break; // Becher 1: 180 Grad
        case 2: angle = 120; break; // Becher 2: 120 Grad
        case 3: angle = 50; break;  // Becher 3: 50 Grad
        case 4: angle = 0; break;   // Becher 4: 0 Grad
        default: return; // Beendet die Funktion, falls eine ungültige Nummer übergeben wird
    }
    Serial.print("Bewege Servo zu Becher ");
    Serial.println(cupNumber); // Gibt die Bechernummer aus
    setAngle(angle); // Ruft setAngle auf, um den Servo auf den gewählten Winkel zu setzen
}
