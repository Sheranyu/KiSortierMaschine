#ifndef Button_h
#define Button_h

#include <Arduino.h> // Inkludiert die Arduino-Bibliothek für Hardware-Funktionen.

// Deklariert die Klasse Button zur Handhabung eines Hardware-Buttons.
class Button {
public:
    Button(int pin); // Konstruktor, der den Pin des Buttons festlegt.
    void update(); // Überprüft den Zustand des Buttons und führt ggf. die Callback-Funktion aus.
    void setMotorControlCallback(void (*callback)(bool)); // Setzt die Callback-Funktion, die aufgerufen wird, wenn der Button gedrückt wird.

private:
    int buttonPin; // Pinnummer, an dem der Button angeschlossen ist.
    bool lastButtonState; // Der letzte gelesene Zustand des Buttons.
    bool currentButtonState; // Der aktuelle Zustand des Buttons.
    unsigned long lastDebounceTime; // Zeitpunkt der letzten Zustandsänderung zur Entprellung.
    unsigned long debounceDelay; // Verzögerung für die Entprellung in Millisekunden.
    void (*motorControlCallback)(bool); // Pointer auf die Callback-Funktion.
};

#endif