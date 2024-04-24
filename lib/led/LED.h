#ifndef LED_h
#define LED_h

#include <Arduino.h>  // Einbinden der Arduino-Hauptbibliothek

// Definiert die Klasse LED zur Steuerung einer RGB-LED
class LED {
public:
  LED(int pinR, int pinG, int pinB);  // Konstruktor, der Pins für Rot, Grün und Blau erhält
  void setColor(int R, int G, int B);  // Methode zum Einstellen der Farbe über RGB-Werte
  void setColorByName(String colorName);  // Methode zum Einstellen der Farbe anhand eines Namens

private:
  int pinRed, pinGreen, pinBlue;  // Speichert die Pinnummern für die jeweiligen LED-Farben
};

#endif
