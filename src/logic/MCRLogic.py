from asyncio import StreamReader, StreamWriter
import asyncio
import serial
import time

from sqlalchemy import null
import serial_asyncio
from StatusMeldungen.status import MCRMeldungen, WarnStatus
from modele.InterneDatenModele import KiData, LeuchtFarbenLampe, SchnazenSteuerungFarbe

COMMODE = "COM6"
async def recv(stream: StreamReader):
    return await stream.readline()

class SerialInit:
    async def _initserial(self):
        self.timeout = 0
        self.TIMEOUTEND = 5
        self.reader ,self.writer = await serial_asyncio.open_serial_connection(url=COMMODE, baudrate=115200)

class SchwanzenBewegungNachFarbe(SerialInit):
    def __init__(self):
        super().__init__()

       
    async def start_changeposition(self, kilaufdaten: KiData):
        label = kilaufdaten.label_name.strip()
    
        if label in SchnazenSteuerungFarbe.BLUE.value:
            print("blue")
            await self._ChangePosition("b1")
        if label in SchnazenSteuerungFarbe.GREEN.value:
            print("green")
            await self._ChangePosition("b2")
        
        if label in SchnazenSteuerungFarbe.ROT.value:
            print("rot")
            await self._ChangePosition("b3")
        
        if label in SchnazenSteuerungFarbe.SONSTIGES.value:
            await self._ChangePosition("b4")
            
    async def _ChangePosition(self, Positionsnummer: str):
        await self._initserial()
        try:
            print(Positionsnummer)
            data_to_send = Positionsnummer
            self.writer.write(data_to_send.encode())
           
            response = b""
            while response.rstrip() != MCRMeldungen.SERVO_GEDREHT:
                response = await asyncio.wait_for(recv(self.reader),timeout=5)
             
            return   
        finally:
            self.writer.close()
            await self.writer.wait_closed()
    
    
    async def start_raddrehen(self):
        #if kilaufdaten.label_name == SchnazenSteuerungFarbe.BACKGROUND.value:
        await self._raddrehen()  
            
    async def _raddrehen(self):
        try:
            await self._initserial()
            data_to_send = "go"
            self.writer.write(data_to_send.encode())
            
            response = ""
            while response.rstrip() != MCRMeldungen.GEDREHT:
                response = await asyncio.wait_for(recv(self.reader),timeout=5)

            return
        finally:
            self.writer.close()
            await self.writer.wait_closed()
            
            
class LedSteuerung(SerialInit):
    def __init__(self) -> None:
        super().__init__()
        
    async def setledcolor(self,kilaufdaten: KiData):
        
       
        label = kilaufdaten.label_name.strip()

        if label in SchnazenSteuerungFarbe.BLUE.value:
            await self._change_color(LeuchtFarbenLampe.BLAU)
        elif label in SchnazenSteuerungFarbe.GREEN.value:
            await self._change_color(LeuchtFarbenLampe.GRUEN)
        
        elif label in SchnazenSteuerungFarbe.ROT.value:
            await self._change_color(LeuchtFarbenLampe.ROT)
        
        elif label in SchnazenSteuerungFarbe.SONSTIGES.value:
            await self._change_color(LeuchtFarbenLampe.SONSTIGES)
        else:
            print("Dürfte nicht hier drin sein zeile 95: LEDSteuerung")
     
    async def _change_color(self, ledcolor: LeuchtFarbenLampe):
        try:
            await self._initserial()
            data_to_send = ledcolor.value.strip()
            self.writer.write(data_to_send.encode())
            
            response = ""
            while response.rstrip() != MCRMeldungen.LED_UMGESCHALTET:
                response = asyncio.wait_for(await recv(self.reader),timeout=5)
            # await asyncio.sleep(0.1)
            # self.timeout += 0.1
            # if self.timeout> self.TIMEOUTEND:
            #     raise TimeoutError(WarnStatus.TIMEOUT_WARN)
        finally:
            self.writer.close()
            await self.writer.wait_closed()