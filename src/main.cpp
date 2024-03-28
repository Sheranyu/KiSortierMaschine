#include <Arduino.h>

void setup() {
  // Initialisieren der seriellen Kommunikation mit der Baudrate von 115200
  Serial.begin(9600);
}

void loop() {
  // Prüfen, ob Daten verfügbar sind
  if (Serial.available() > 0) {
    // Lesen des eingehenden Zeichens
    char c = Serial.read();
    
    // Ausgabe des empfangenen Zeichens zurück an den Sender
    Serial.print(c);
  }
}
