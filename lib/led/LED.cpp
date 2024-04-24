#include "LED.h"  // Inkludiert die Definition der LED-Klasse

// Konstruktor der Klasse LED
LED::LED(int pinR, int pinG, int pinB) {
  pinRed = pinR;  // Setzt den Pin für die rote LED
  pinGreen = pinG;  // Setzt den Pin für die grüne LED
  pinBlue = pinB;  // Setzt den Pin für die blaue LED
  pinMode(pinRed, OUTPUT);  // Konfiguriert den Roten Pin als Ausgang
  pinMode(pinGreen, OUTPUT);  // Konfiguriert den Grünen Pin als Ausgang
  pinMode(pinBlue, OUTPUT);  // Konfiguriert den Blauen Pin als Ausgang
}

// Setzt die Farbe der LED durch direkte Angabe der RGB-Werte
void LED::setColor(int R, int G, int B) {
  analogWrite(pinRed, R);  // Setzt die Intensität der roten LED
  analogWrite(pinGreen, G);  // Setzt die Intensität der grünen LED
  analogWrite(pinBlue, B);  // Setzt die Intensität der blauen LED
  Serial.println("led_umgeschaltet");  // Gibt eine Nachricht über den Farbwechsel aus
}

// Setzt die LED-Farbe basierend auf einem übergebenen Farbnamen
void LED::setColorByName(String colorName) {
    // Überprüft den Farbnamen und setzt die entsprechenden RGB-Werte
    if (colorName == "rot" || colorName == "red") {
        setColor(255, 0, 0);  // Rot
    } else if (colorName == "gruen" || colorName == "green") {
        setColor(0, 255, 0);  // Grün
    } else if (colorName == "blau" || colorName == "blue") {
        setColor(0, 0, 255);  // Blau
    } else if (colorName == "lila" || colorName == "purple") {
        setColor(153, 0, 153);  // Lila
    } else if (colorName == "weiss" || colorName == "white") {
        setColor(255, 255, 255);  // Weiß
    } else if (colorName == "schwarz" || colorName == "black") {
        setColor(0, 0, 0);  // Schwarz
    } else if (colorName == "gelb" || colorName == "yellow") {
        setColor(158, 94, 0);  // Gelb
    } else if (colorName == "sonstig" || colorName == "other") {
        setColor(0, 255, 255);  // Cyan
    } else {
        Serial.println("Unbekannter Farbbefehl: " + colorName);  // Meldung bei unbekanntem Farbnamen
    }
}