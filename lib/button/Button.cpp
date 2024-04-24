#include "Button.h" // Inkludiert die Definition der Button-Klasse.

// Konstruktor: Initialisiert die Eigenschaften des Buttons.
Button::Button(int pin) : buttonPin(pin), lastButtonState(LOW), currentButtonState(LOW), lastDebounceTime(0), debounceDelay(50), motorControlCallback(nullptr) {
  pinMode(buttonPin, INPUT_PULLUP); // Setzt den Button-Pin als Eingang mit aktiviertem internen Pull-Up-Widerstand.
}

// Überprüft regelmäßig den Zustand des Buttons und verarbeitet Zustandsänderungen.
void Button::update() {
  bool reading = digitalRead(buttonPin); // Liest den aktuellen Zustand des Button-Pins.
  if (reading != lastButtonState) { // Überprüft auf eine Zustandsänderung.
    lastDebounceTime = millis(); // Setzt die Zeit der letzten Zustandsänderung zurück.
  }
  if ((millis() - lastDebounceTime) > debounceDelay) { // Überprüft, ob die Entprellzeit abgelaufen ist.
    if (reading != currentButtonState) { // Bestätigt die Zustandsänderung nach Ablauf der Entprellzeit.
      currentButtonState = reading; // Aktualisiert den aktuellen Zustand des Buttons.
      if (currentButtonState == LOW) { // Überprüft, ob der Button gedrückt ist (niedrig, wenn gedrückt wegen Pull-Up-Widerstand).
        if (motorControlCallback != nullptr) { // Überprüft, ob eine Callback-Funktion gesetzt ist.
          motorControlCallback(!currentButtonState); // Ruft die Callback-Funktion mit dem gedrückten Zustand auf.
        }
      }
    }
  }
  lastButtonState = reading; // Aktualisiert den letzten gelesenen Zustand des Buttons.
}

// Setzt eine Callback-Funktion, die aufgerufen wird, wenn der Button gedrückt wird.
void Button::setMotorControlCallback(void (*callback)(bool)) {
  motorControlCallback = callback; // Speichert den Pointer auf die Callback-Funktion.
}

