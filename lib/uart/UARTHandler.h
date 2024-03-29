#ifndef UARTHandler_h
#define UARTHandler_h

#include <Arduino.h>

class UARTHandler {
  public:
    UARTHandler();
    void processInput();
    void setMotorRunning(bool running);
    void setServoAngle(int angle);

    bool isMotorRunning() const { return motorRunning; }

    void changeMotorDirection(bool dir);

  private:
    String incomingCommand;
    bool motorRunning;
};

#endif
