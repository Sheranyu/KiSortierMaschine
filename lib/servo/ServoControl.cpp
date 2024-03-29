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
