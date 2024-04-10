import serial
import time

from sqlalchemy import null

from modele.InterneDatenModele import KiData, SchnazenSteuerungFarbe



class SchwanzenBewegungNachFarbe():
    
    def _initserial(self):
        self.ser = serial.Serial('COM6', 115200)
        self.timeout = 0
        self.TIMEOUTEND = 5
       
    def start_changeposition(self, kilaufdaten: KiData):
        label = kilaufdaten.label_name

        if label == SchnazenSteuerungFarbe.BLAU.value:
            self._ChangePosition("b1")
        if label == SchnazenSteuerungFarbe.GRUEN.value:
            self._ChangePosition("b2")
        
        if label == SchnazenSteuerungFarbe.ROT.value:
            self._ChangePosition("b3")
        
        if label == SchnazenSteuerungFarbe.SONSTIGES.value:
            self._ChangePosition("b4")
            
    def _ChangePosition(self, Positionsnummer: str):
        self._initserial()
        try:
            data_to_send = Positionsnummer
            self.ser.write(data_to_send.encode())
            time.sleep(1)
            while not response:
                response = self.ser.readline().decode().strip()
                time.sleep(0.1)
                self.timeout += 0.1
                if self.timeout> self.TIMEOUTEND:
                    raise TimeoutError("Zeitüberschreitung")
                
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
        
        
        while response != "gedreht":
            response = self.ser.readline().decode().strip()
            time.sleep(0.1)
            self.timeout += 0.1
            if self.timeout> self.TIMEOUTEND:
                raise TimeoutError("Zeitüberschreitung")
                
        return
            
            
            
            
     
    