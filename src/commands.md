# Befehlsübersicht für das Arduino-Projekt

Diese Datei bietet eine Übersicht über alle verfügbaren UART-Befehle, ihre Funktionen und Beispiele für ihre Verwendung.

## Befehle

### Starten des Steppermotors
- **Beschreibung**: Startet den Steppermotor.
- **Befehl**: `start;`



### Stoppen des Steppermotors
- **Beschreibung**: Stoppt den Steppermotor.
- **Befehl**: `stop;`



### Einstellen der Drehrichtung des Steppermotors
- **Beschreibung**: Ändert die Drehrichtung des Steppermotors. `1` für im Uhrzeigersinn, `0` für gegen den Uhrzeigersinn.
- **Befehl**: `dir{Richtung};`
- **Beispiele**:
- Im Uhrzeigersinn:
  ```
  dir1;
  ```
- Gegen den Uhrzeigersinn:
  ```
  dir0;
  ```

### Einstellen der Servoposition
- **Beschreibung**: Einstellen der Position des Servomotors. Die Position sollte eine Zahl zwischen 0 und 180 sein.
- **Befehl**: `sg1{Position};`
- **Beispiel**:
- Auf 120 Grad drehen:
  ```
  sg1120;
  ```



### Einstellen der LED-Farbe
- **Beschreibung**: Einstellen der Farbe der LED über RGB-Werte. Jeder Wert kann zwischen 0 und 255 liegen.
- **Befehl**: `led{Rot}{Grün}{Blau};`
- **Beispiele**:
- Rotes Licht:
  ```
  led255000000;
  ```
- Grünes Licht:
  ```
  led000255000;
  ```
- Blaues Licht:
  ```
  led000000255;
  ```

### Unbekannter Befehl
- **Beschreibung**: Wird ausgegeben, wenn ein eingegebener Befehl nicht erkannt wird.
