#ifndef UARTHandler_h
#define UARTHandler_h

#include <Arduino.h>
#include "LED.h"

class UARTHandler {
  public:
    UARTHandler(LED& led);
    void processInput();
    void setMotorRunning(bool running);
    void setServoAngle(int angle);

    bool isMotorRunning() const { return motorRunning; }

    void changeMotorDirection(bool dir);

    void processLEDCommand(String command);

  private:
    String incomingCommand;
    bool motorRunning;
    LED& ledObj; // Referenz auf das LED-Objekt
};

#endif
