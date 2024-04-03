#include "StepperMotor.h"

StepperMotor::StepperMotor(int pin1, int pin2, int pin3, int pin4) : totalSteps(0) {
  pins[0] = pin1;
  pins[1] = pin2;
  pins[2] = pin3;
  pins[3] = pin4;
  for (int i = 0; i < 4; i++) {
    pinMode(pins[i], OUTPUT);
  }
  stepNumber = 0;
}

void StepperMotor::setDirection(bool dir) {
  direction = dir;
}

void StepperMotor::oneStep(bool dir) {
  int stepCount = 4;  // Anzahl der Schritte in deiner Sequenz
  digitalWrite(pins[stepNumber % 4], LOW);  // Schalte den aktuellen Pin aus
  if (direction) {
    stepNumber++;
  } else {
    stepNumber--;
  }
  if (stepNumber >= stepCount) {
    stepNumber = 0;
  } else if (stepNumber < 0) {
    stepNumber = stepCount - 1;
  }
  digitalWrite(pins[stepNumber % 4], HIGH);  // Schalte den nächsten Pin ein
}

void StepperMotor::setRunning(bool running) {
    this->running = running;
}

void StepperMotor::runIfNeeded() {
    if (running) {
        oneStep(direction); // Richtung ist bereits als Zustand gespeichert
        delay(10); // Anpassbare Verzögerung zur Geschwindigkeitskontrolle
    }
}

void StepperMotor::moveSteps(int steps) {
  // Serial.print("Gehe folgende Anzahl an Schritten: "); // Zum Debuggen, ob Abgleich funktioniert, siehe Funktion goCommandReceived
  // Serial.println(steps); // Zum Debuggen, ob Abgleich funktioniert, siehe Funktion goCommandReceived
    for(int i = 0; i < abs(steps); i++) {
        oneStep(steps > 0);
        totalSteps += (steps > 0) ? 1 : -1;
        delay(10); // Kurze Verzögerung für den Schritt
    }
    Serial.println("gedreht");
}

void StepperMotor::goToInitialPosition() {
    moveSteps(-totalSteps); // Bewegt sich zurück zur angenommenen Startposition
    totalSteps = 0; // Setzt die Gesamtzahl der Schritte zurück
}

void StepperMotor::setStepsPerRevolution(int steps) {
    stepsPerRevolution = steps;
}

int StepperMotor::getStepsForDegrees(int degrees) {
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

    goCommandCount++;
    const int stepsFor120Degrees = getStepsForDegrees(120); // Berechnet die Schritte für 120°

    if (goCommandCount % 3 == 0) { // Jedes dritte Mal
        Serial.print("\nDrehe den Steppermotor um 120° (");
        Serial.print(stepsFor120Degrees + 2);
        Serial.println(" Schritte)");
        moveSteps(stepsFor120Degrees + 2); // Bewegt den Motor um die berechneten Schritte, füge 2 zusätzliche Schritte hinzu, um die Abweichung auszugleichen
    }
    else if (goCommandCount % 3 != 0) { // Jedes Mal, außer jedes dritte Mai
        Serial.print("\nDrehe den Steppermotor um 120° (");
        Serial.print(stepsFor120Degrees);
        Serial.println(" Schritte)");
        moveSteps(stepsFor120Degrees); // Bewegt den Motor um die berechneten Schritte
    }
}