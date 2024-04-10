#include "ServoControl.h"

ServoControl::ServoControl(int pin) : servoPin(pin), lastUpdate(0) {}

void ServoControl::attach() {
    servo.attach(servoPin);
}

void ServoControl::testServo() {
    isTesting = !isTesting; // Umschalten des Testmodus
}

void ServoControl::update() {
    if (isTesting) {
        unsigned long currentMillis = millis();
        if (currentMillis - lastUpdate > 15) { // Bewege den Servo alle 15ms
            lastUpdate = currentMillis;
            angle += direction;
            if (angle >= 180 || angle <= 0) {
                direction = -direction; // Richtung umkehren
                angle += direction; // Stellt sicher, dass angle innerhalb der Grenzen bleibt
            }
            servo.write(angle);
        }
    }
}

void ServoControl::setAngle(int angle) {
    if (angle >= 0 && angle <= 180) {
        this->angle = angle; // Speichere den Winkel für den nächsten Update-Zyklus
        servo.write(angle); // Setze den Winkel sofort
    }
    Serial.print("servo_gedreht");
}

void ServoControl::moveToCup(int cupNumber) {
    int angle;
    switch (cupNumber) {
        case 1: angle = 180; break; // Becher 1: 180 Grad
        case 2: angle = 120; break; // Becher 2: 120 Grad
        case 3: angle = 50; break;  // Becher 3: 50 Grad
        case 4: angle = 0; break;   // Becher 4: 0 Grad
        default: return; // Ungültige Bechernummer
    }
    Serial.print("Bewege Servo zu Becher ");
    setAngle(angle);
    Serial.println(cupNumber);
}