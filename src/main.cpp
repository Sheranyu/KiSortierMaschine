#include <Arduino.h>
#include <Servo.h>

void setColor(int R, int G, int B);
void OneStep(bool dir);


#define STEPPER_PIN_1 PA5
#define STEPPER_PIN_2 PA6
#define STEPPER_PIN_3 PA7
#define STEPPER_PIN_4 PA8

#define SERVO_PIN PB7

#define LED_PIN_RED PC5
#define LED_PIN_GREEN PC6
#define LED_PIN_BLUE PC8

#define BUTTON_PIN PC9


int step_number = 0;
bool motorRunning = false; // Zustandsvariable für den Motor

const int PIN_RED   = LED_PIN_RED;
const int PIN_GREEN = LED_PIN_GREEN;
const int PIN_BLUE  = LED_PIN_BLUE;

const int buttonPin = BUTTON_PIN;  // the number of the pushbutton pin


Servo servo;
int angle = 1; // Startwinkel
bool isMoving = false; // Variable, um den Bewegungsstatus zu speichern


String incomingCommand = ""; // Eine String-Variable zum Speichern des eingehenden Befehls

void setup() 
{
  Serial.begin(9600); // Initialisiere serielle Kommunikation
  servo.attach(SERVO_PIN); // Attach the servo on pin PA9 to the servo object

  pinMode(STEPPER_PIN_1, OUTPUT);
  pinMode(STEPPER_PIN_2, OUTPUT);
  pinMode(STEPPER_PIN_3, OUTPUT);
  pinMode(STEPPER_PIN_4, OUTPUT);

  pinMode(PIN_RED,   OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BLUE,  OUTPUT);

  // Initialisieren der seriellen Kommunikation mit der Baudrate von 115200
}

void loop() 
{
  // Setze die Farbe zu Weiß (#FFFFFF)
  setColor(255, 255, 255);

  // Prüfen, ob Daten verfügbar sind
  if (Serial.available() > 0) 
  {
    // Lesen des eingehenden Zeichens
    char receivedChar = Serial.read();
    // Direkte Ausgabe des empfangenen Zeichens zurück an den Sender
    Serial.print(receivedChar);
    
    // Überprüfen, ob das empfangene Zeichen ein Befehlstrennzeichen ist
    if (receivedChar == ';' || receivedChar == '\n' || receivedChar == '\r') 
    {
      if (incomingCommand.startsWith("start")) 
      {
        Serial.println("\nStarte Schrittmotor...");
        // Hier die Logik für den Start-Befehl einfügen
        motorRunning = true; // Starte den Schrittmotor
      }
      else if (incomingCommand.startsWith("stop"))
      {
        Serial.println("\nStoppe Schrittmotor...");
        motorRunning = false; // Stoppe den Schrittmotor
      }
      else if (incomingCommand.startsWith("sg1")) // Überprüft, ob der Befehl mit "sg1" beginnt
      { 
        int newAngle = incomingCommand.substring(3).toInt(); // Extrahiert den Winkel aus dem Befehl
        if (newAngle >= 0 && newAngle <= 180) // Überprüft, ob der Winkel gültig ist
        { 
          Serial.println("\nSetze Servoposition...");
          servo.write(newAngle); // Bewegt den Servo auf den neuen Winkel
        }
      }
      else if (incomingCommand.length() > 0) // Vermeidung der Ausgabe bei leerem Befehl
      {
        Serial.println("\nUnknown command: " + incomingCommand);
      }
      // Zurücksetzen des Befehlsstrings für den nächsten Befehl
      incomingCommand = "";
    } 
    else 
    {
      // Füge das Zeichen zum Befehlsstring hinzu, wenn es sich nicht um ein Trennzeichen handelt
      incomingCommand += receivedChar;
    }
  }


  if (motorRunning) 
  {
    OneStep(false);
    delay(6);
  }

}



void OneStep(bool dir) 
{
  if (dir) 
  {
    switch (step_number) 
    {
      case 0:
        digitalWrite(STEPPER_PIN_1, HIGH);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 1:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, HIGH);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 2:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, HIGH);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 3:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, HIGH);
        break;
    }
  } 
  else 
  {
    switch (step_number) 
    {
      case 0:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, HIGH);
        break;
      case 1:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, HIGH);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 2:
        digitalWrite(STEPPER_PIN_1, LOW);
        digitalWrite(STEPPER_PIN_2, HIGH);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, LOW);
        break;
      case 3:
        digitalWrite(STEPPER_PIN_1, HIGH);
        digitalWrite(STEPPER_PIN_2, LOW);
        digitalWrite(STEPPER_PIN_3, LOW);
        digitalWrite(STEPPER_PIN_4, LOW);
    }
  }
  step_number++;
  if (step_number > 3) {
    step_number = 0;
  }
}



void setColor(int R, int G, int B) 
{
  analogWrite(PIN_RED,   R);
  analogWrite(PIN_GREEN, G);
  analogWrite(PIN_BLUE,  B);
}
