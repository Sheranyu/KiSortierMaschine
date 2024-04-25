#include "StepperMotor.h" // Inkludiert die Header-Datei für die StepperMotor-Klasse.

#define STEPPER_SPEED 2 // in ms

// Konstruktor der Klasse StepperMotor, der die Pins für die Motoransteuerung initialisiert.
StepperMotor::StepperMotor(int pin1, int pin2, int pin3, int pin4) : totalSteps(0) {
  // Zuweisen der Pins zu einem Array, welches die Steuerung des Schrittmotors ermöglicht.
  pins[0] = pin1; // Zuweisung des ersten Motorsteuerungspins.
  pins[1] = pin2; // Zuweisung des zweiten Motorsteuerungspins.
  pins[2] = pin3; // Zuweisung des dritten Motorsteuerungspins.
  pins[3] = pin4; // Zuweisung des vierten Motorsteuerungspins.

  // Schleife zum Setzen der Pin-Modi für die Motorsteuerung.
  for (int i = 0; i < 4; i++) {
    pinMode(pins[i], OUTPUT); // Setzt jeden der Motorpins als Ausgang.
  }

  // Initialisiert den stepNumber-Index auf 0, startet die Schrittsequenz von Anfang.
  stepNumber = 0;
}

// Setzt die Drehrichtung des Schrittmotors.
void StepperMotor::setDirection(bool dir) {
  direction = dir; // Speichert die angegebene Richtung im Zustandsattribut 'direction'.
}

// Führt einen einzelnen Schritt des Schrittmotors aus, basierend auf der aktuellen Drehrichtung.
void StepperMotor::oneStep(bool dir) {
  int stepCount = 4;  // Anzahl der Schritte in deiner Sequenz, typisch für 4-Phasen-Schrittmotoren.

  // Deaktiviert den aktuellen Motorpin, um den Schritt vorzubereiten.
  digitalWrite(pins[stepNumber % 4], LOW);  // Schaltet den aktuellen Pin aus, moduliert durch die aktuelle Schrittnummer.

  // Entscheidet, ob die Schrittnummer erhöht oder verringert wird, basierend auf der globalen Richtungsvariable `direction`.
  if (direction) {
    stepNumber++;  // Erhöht die Schrittnummer, wenn die Drehrichtung vorwärts ist.
  } else {
    stepNumber--;  // Verringert die Schrittnummer, wenn die Drehrichtung rückwärts ist.
  }

  // Überprüft und passt die Schrittnummer an, um sicherzustellen, dass sie innerhalb des gültigen Bereichs bleibt.
  if (stepNumber >= stepCount) {
    stepNumber = 0;  // Setzt die Schrittnummer zurück auf 0, wenn das Ende der Schrittsequenz erreicht ist.
  } else if (stepNumber < 0) {
    stepNumber = stepCount - 1;  // Setzt die Schrittnummer auf den höchsten Wert der Sequenz, wenn sie negativ wird.
  }

  // Aktiviert den nächsten Motorpin für den nächsten Schritt.
  digitalWrite(pins[stepNumber % 4], HIGH);  // Schaltet den nächsten Pin ein, moduliert durch die aktuelle Schrittnummer.
}

// Steuert den Betriebszustand des Schrittmotors.
void StepperMotor::setRunning(bool running) {
  this->running = running;  // Setzt die Zustandsvariable `running`, die bestimmt, ob der Motor aktiv ist oder nicht.
}

void StepperMotor::runIfNeeded() {
    if (running) {
        oneStep(direction); // Richtung ist bereits als Zustand gespeichert
        delay(STEPPER_SPEED); // Anpassbare Verzögerung zur Geschwindigkeitskontrolle
    }
}

void StepperMotor::moveSteps(int steps) {
  // Serial.print("Gehe folgende Anzahl an Schritten: "); // Zum Debuggen, ob Abgleich funktioniert, siehe Funktion goCommandReceived
  // Serial.println(steps); // Zum Debuggen, ob Abgleich funktioniert, siehe Funktion goCommandReceived
    for(int i = 0; i < abs(steps); i++) {
        oneStep(steps > 0);
        totalSteps += (steps > 0) ? 1 : -1;
        delay(STEPPER_SPEED); // Kurze Verzögerung für den Schritt
    }
    Serial.println("gedreht");
}

void StepperMotor::goToInitialPosition() {
    moveSteps(-totalSteps); // Bewegt sich zurück zur angenommenen Startposition
    totalSteps = 0; // Setzt die Gesamtzahl der Schritte zurück
}

// Setzt die Anzahl der Schritte, die der Schrittmotor für eine vollständige 360° Umdrehung benötigt.
void StepperMotor::setStepsPerRevolution(int steps) {
    stepsPerRevolution = steps;  // Speichert die Anzahl der Schritte pro Umdrehung in der Instanzvariablen.
}

// Berechnet die Anzahl der Schritte, die der Schrittmotor machen muss, um sich um eine bestimmte Anzahl von Grad zu drehen.
int StepperMotor::getStepsForDegrees(int degrees) {
    // Berechnet und gibt die Schritte zurück, indem die Anzahl der Schritte pro Umdrehung
    // mit der Anzahl der gewünschten Grad multipliziert und durch 360 geteilt wird.
    // Diese Formel konvertiert Grad in eine proportionale Anzahl von Schritten.
    return stepsPerRevolution * degrees / 360;
}

void StepperMotor::goCommandReceived() {

  /*
  Diese Funktion ist dazu gedacht, die Schritte des Schrittmotors auszugleichen. Da der Schrittmorot für eine volle Umdrehung 2048 Schritte (360°) benötigt,
  und das Rad 3 Einschübe hat, muss der Schrittmotor sich immer um 2048 / 3 Schritte umdrehen (360° / 3 = 120°).
  2048 / 3 ergeben allerdings 682,667...
  Da die Schritte als int gesteuert werden, wird der Kommabereich abgeschnitten und der Motor dreht nur 628 Schritte.
  Dies würde, je mehr Dreh-Befehle an den Motor gesendet werden, zu einer immer größeren Abweichung führen.
  Um dies zu verhindern, werden bei jedem dritten Befehl immer 2 Schritte addiert,
  da 682,667 * 3  2048 ergeben und (682 * 3) +2 auch 2048 ergeben, was die einmalige Umdrehung der eigenen Achse des Motors entspricht.
  Somit ist sichergestellt, das der Motor je mehr Dreh-Befehle versendet werden, nicht abweicht.
  */

    goCommandCount++;  // Erhöht den Zähler für die "go"-Befehle um eins.

    // Berechnet die erforderlichen Schritte, um den Motor um 120° zu drehen.
    const int stepsFor120Degrees = getStepsForDegrees(120); // Berechnet die Schritte für 120°.

    // Überprüft, ob der aktuelle "go"-Befehl der dritte in der Reihe ist.
    if (goCommandCount % 3 == 0) { // Jedes dritte Mal
        Serial.print("\nDrehe den Steppermotor um 120° (");
        Serial.print(stepsFor120Degrees + 2);
        Serial.println(" Schritte)");  // Informiert über die Anzahl der Schritte, einschließlich der Korrektur.
        moveSteps(stepsFor120Degrees + 2); // Bewegt den Motor um die berechneten Schritte plus zwei zusätzliche, um die Abweichung auszugleichen.
    }
    else { // Für alle anderen "go"-Befehle, die nicht die dritten sind.
        Serial.print("\nDrehe den Steppermotor um 120° (");
        Serial.print(stepsFor120Degrees);
        Serial.println(" Schritte)");  // Informiert über die Anzahl der berechneten Schritte ohne Korrektur.
        moveSteps(stepsFor120Degrees); // Bewegt den Motor um die berechneten Schritte.
    }
}