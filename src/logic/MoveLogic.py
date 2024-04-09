import serialsteuererung
import time

from sqlalchemy import null

from modele.InterneDatenModele import KiData, SchnazenSteuerungFarbe



class SchwanzenBewegungNachFarbe():
    
    def _initserial(self):
        self.ser = serialsteuererung.Serial('/dev/ttyUSB0', 9600)
       
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
            while True:  
                # Antwort vom Arduino lesen
                
                    response = self.ser.readline().decode().strip()
                    if response:
                        return
                    time.sleep(0.3)
        except:
            self.ser.close()
            print("Program terminated.")
    
    
    
    def start_raddrehen(self, kilaufdaten: KiData):
        if kilaufdaten.label_name == SchnazenSteuerungFarbe.BACKGROUND.value:
            self._raddrehen()  
            
    def _raddrehen(self):
        self._initserial()
        data_to_send = "go"
        self.ser.write(data_to_send.encode())
        
        
        while True:
            response = self.ser.readline().decode().strip()
            if response == "gedreht":
                self.ser.close()
                return
            
            time.sleep(0.3)
            
            
     
    