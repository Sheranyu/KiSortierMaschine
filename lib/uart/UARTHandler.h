#ifndef UARTHandler_h
#define UARTHandler_h

#include <Arduino.h>
#include "LED.h"
#include "ServoControl.h"

class UARTHandler {
  public:
    UARTHandler(LED& led);
    void processInput();
    void setMotorRunning(bool running);
    void setServoAngle(int angle);

    bool isMotorRunning() const { return motorRunning; }

    void changeMotorDirection(bool dir);

    void processLEDCommand(String command);

    void setServoControl(ServoControl& servoControl) {
        this->servoControl = &servoControl;
    }

  private:
    String incomingCommand;
    bool motorRunning;
    LED& ledObj; // Referenz auf das LED-Objekt
    ServoControl* servoControl; // Zeiger auf das ServoControl-Objekt
};

#endif
