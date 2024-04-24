from asyncio import StreamReader, StreamWriter
import asyncio

from sqlalchemy import null
import serial_asyncio
from StatusMeldungen.status import MCRMeldungen, WarnStatus
from configordner.settings import SaveDictName
from libcomponents.filterdata import filterschanzennachlabel
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import Erkanntermodus, KiData, LeuchtFarbenLampe, SchanzenSteuerungFarbe, SerialConfigModel
from modele.SchanzenModelle import  SchanzenSteuerungformenum, SchanzenSteuerung

COMMODE = "COM6"
async def recv(stream: StreamReader):
    return await stream.readline()

class SerialInit:
    async def _initserial(self):   
        commode = KiDataManager.ladeDaten(SaveDictName.serialsettings, SerialConfigModel)
        
        self.timeout = 0
        self.TIMEOUTEND = 5
        self.reader ,self.writer = await serial_asyncio.open_serial_connection(url=commode.COM, baudrate=115200)
    
    
    def loadschanzendata(self):
        return KiDataManager.ladeSessiondata(SaveDictName.topfmodus,SchanzenSteuerung)
        
class SchanzenBewegung(SerialInit):
    def __init__(self):
        super().__init__()
        
        
    async def start_changeposition(self, kilaufdaten: KiData):
        label = kilaufdaten.label_name.strip()
        topfdata = self.loadschanzendata()
        print(topfdata)
        filtereddata = filterschanzennachlabel(topfdata,label)
        if filtereddata is None:
            return None
        
        return await self._ChangePosition(filtereddata.Topf)
        
        
        # if label in SchanzenSteuerungFarbe.BLUE.value or label in SchanzenSteuerungformenum.acht.value:
        #     print("blue")
        #     await self._ChangePosition("b1")

        # if label in SchanzenSteuerungFarbe.GREEN.value or label in SchanzenSteuerungformenum.sechs.value:
        #     print("green")
        #     await self._ChangePosition("b2")
        
        # if label in SchanzenSteuerungFarbe.ROT.value or label in  SchanzenSteuerungformenum.zwanzig.value:
        #     print("rot")
        #     await self._ChangePosition("b3")
        
        # if label in SchanzenSteuerungFarbe.SONSTIG.value or label in SchanzenSteuerungformenum.sonstig.value:
        #     await self._ChangePosition("b4")
            
    async def _ChangePosition(self, Positionsnummer: str):
        try:

            await self._initserial()
            
            data_to_send = Positionsnummer
            self.writer.write(data_to_send.encode())
            
            response = b""
            while response.rstrip() != MCRMeldungen.SERVO_GEDREHT:
                response = await recv(self.reader)
                print(response)
            response_str = response.decode().strip()
            self.writer.close()
            await self.writer.wait_closed()
            return response_str
        except:
            self.writer.close()
            await self.writer.wait_closed()
       
    
      
    
    
    async def start_raddrehen(self) -> str:
        #if kilaufdaten.label_name == SchnazenSteuerungFarbe.BACKGROUND.value:
        await self._raddrehen()  
    
    
    async def _raddrehen(self) -> str:
        await self._initserial()
        
        data_to_send = "go"
        self.writer.write(data_to_send.encode())
        
        response = b""
        while response.rstrip() != MCRMeldungen.GEDREHT:
            response = await asyncio.wait_for(recv(self.reader),timeout=10)
            print(response)
            

        
        resposne_str = response.decode().strip()
        self.writer.close()
        await self.writer.wait_closed()
        return 
        
            
            
         
class LedSteuerung(SerialInit):
    def __init__(self) -> None:
        pass
    
        
    async def setledcolor(self,kilaufdaten: KiData):
        label = kilaufdaten.label_name.strip()
        topfdata = self.loadschanzendata()
        filtereddata = filterschanzennachlabel(topfdata,label)
        if filtereddata is None:
            return None
        if kilaufdaten.erkannter_modus == Erkanntermodus.FARBE:
            await self._change_color(filtereddata.selected)
        else:
            await self._change_color(filtereddata.formcolor)

        # if label in SchanzenSteuerungFarbe.BLUE.value:
        #     await self._change_color(LeuchtFarbenLampe.BLAU)
        # elif label in SchanzenSteuerungFarbe.GREEN.value:
        #     await self._change_color(LeuchtFarbenLampe.GRUEN)
        
        # elif label in SchanzenSteuerungFarbe.ROT.value:
            
        #     await self._change_color(LeuchtFarbenLampe.ROT)
        
        # elif label == SchanzenSteuerungFarbe.SONSTIG.value:
        #     await self._change_color(LeuchtFarbenLampe.SONSTIGES)
        # else:
        #     print("Dürfte nicht hier drin sein zeile 111: LEDSteuerung")
     
    async def _change_color(self, ledcolor: str):
        try:

            await self._initserial()
            data_to_send = ledcolor.strip()
            self.writer.write(data_to_send.encode())
            
            response = b""
            while response.rstrip() != MCRMeldungen.LED_UMGESCHALTET:
                response = await asyncio.wait_for(recv(self.reader),timeout=10)
            
    
            
            
            # await asyncio.sleep(0.1)
            # self.timeout += 0.1
            # if self.timeout> self.TIMEOUTEND:
            #     raise TimeoutError(WarnStatus.TIMEOUT_WARN)
        
            self.writer.close()
            await self.writer.wait_closed()
        except:
            self.writer.close()
            await self.writer.wait_closed()