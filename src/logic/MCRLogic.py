import serial
import time

from sqlalchemy import null

from StatusMeldungen.status import MCRMeldungen, WarnStatus
from modele.InterneDatenModele import KiData, LeuchtFarbenLampe, SchnazenSteuerungFarbe



class SchwanzenBewegungNachFarbe():
    
    def _initserial(self):
        self.ser = serial.Serial('COM6', 115200)
        self.timeout = 0
        self.TIMEOUTEND = 5
       
    def start_changeposition(self, kilaufdaten: KiData):
        label = kilaufdaten.label_name.strip()

        if label in SchnazenSteuerungFarbe.BLUE.value:
            self._ChangePosition("b1")
        if "green" in SchnazenSteuerungFarbe.GREEN.value:
            self._ChangePosition("b2")
        
        if "rot" in SchnazenSteuerungFarbe.ROT.value:
            self._ChangePosition("b3")
        
        if label in SchnazenSteuerungFarbe.SONSTIGES.value:
            self._ChangePosition("b4")
            
    def _ChangePosition(self, Positionsnummer: str):
        self._initserial()
        try:
            
            data_to_send = Positionsnummer
            self.ser.write(data_to_send.encode())
            time.sleep(1)
            response = ""
            while response != MCRMeldungen.SERVO_GEDREHT:
                response = self.ser.readline().decode().strip()
                time.sleep(0.1)
                self.timeout += 0.1
                if self.timeout> self.TIMEOUTEND:
                    raise TimeoutError(WarnStatus.TIMEOUT_WARN)
            self.ser.close() 
            return
        except:
            self.ser.close()
            print("Program terminated.")
    
    
    
    def start_raddrehen(self):
        #if kilaufdaten.label_name == SchnazenSteuerungFarbe.BACKGROUND.value:
        self._raddrehen()  
            
    def _raddrehen(self):
        self._initserial()
        data_to_send = "go"
        self.ser.write(data_to_send.encode())
        
        response = ""
        while response != MCRMeldungen.GEDREHT:
            response = self.ser.readline().decode().strip()
            time.sleep(0.1)
            self.timeout += 0.1
            if self.timeout> self.TIMEOUTEND:
                raise TimeoutError(WarnStatus.TIMEOUT_WARN)
        self.ser.close()     
        return
            
            
class LedSteuerung():
    def _initserial(self):
        self.ser = serial.Serial('COM6', 115200)
        self.timeout = 0
        self.TIMEOUTEND = 5     
    
    def setledcolor(self,kilaufdaten: KiData):
        self._initserial()
        label = kilaufdaten.label_name.strip()

        if label in SchnazenSteuerungFarbe.BLUE.value:
            self._change_color(LeuchtFarbenLampe.BLAU)
        elif label in SchnazenSteuerungFarbe.GREEN.value:
            self._change_color(LeuchtFarbenLampe.GRUEN)
        
        elif label in SchnazenSteuerungFarbe.ROT.value:
            self._change_color(LeuchtFarbenLampe.ROT)
        
        elif label in SchnazenSteuerungFarbe.SONSTIGES.value:
            self._change_color(LeuchtFarbenLampe.SONSTIGES)
        else:
            print("Dürfte nicht hier drin sein zeile 95: LEDSteuerung")
     
    def _change_color(self, ledcolor: LeuchtFarbenLampe):
        data_to_send = ledcolor.value.strip()
        self.ser.write(data_to_send.encode())
        
        response = ""
        while response != MCRMeldungen.LED_UMGESCHALTET:
            response = self.ser.readline().decode().strip()
            time.sleep(0.1)
            self.timeout += 0.1
            if self.timeout> self.TIMEOUTEND:
                raise TimeoutError(WarnStatus.TIMEOUT_WARN)
        self.ser.close() 