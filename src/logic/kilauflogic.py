import asyncio
import datetime
from io import TextIOWrapper
import time

import flet as ft
from sqlalchemy.orm import Session
from Ki.opencvcode import TrainiertesModel
from configordner.settings import LaufZeitConfig, SaveDictName
from db.CRUD.EndStatistik import EndStatistik
from logic.KiDatenManager import KiDataManager
from logic.MCRLogic import LedSteuerung, SchanzenBewegungNachFarbe
from modele.InterneDatenModele import Erkanntermodus, KiData
from typing import Any, Generator, List
from datetime import datetime
import pandas as pd

from db.CRUD.Statistik import  StatistikCreater
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.db_and_models.session import sessiongen




class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.aktuellelaufzeit = None
        self.currentkidata: KiData = None
        self.kidatenlist: List[KiData] = []
        self.schanze = SchanzenBewegungNachFarbe()
        self.isamdrehen = False
        self.colorchange = LedSteuerung()
        self.ismoveschanzeaktiv = False
       
    
    def start_application(self,callback,progressring :ft.ProgressRing, callbackinfos) -> Generator[KiData,Any, Any]:
        asyncio.run(self._start_async_app(callback,progressring,callbackinfos))
    

    async def _start_async_app(self, callback, progressring: ft.ProgressRing, callbackinfos) -> None:
        queue = asyncio.Queue()
        # Starte beide Funktionen asynchron
        task1 = asyncio.create_task(self._startasync(queue, progressring, callback, callbackinfos))
        task2 = asyncio.create_task(self._start_ki_verarbeitung(queue))
        await asyncio.gather(task1, task2)

    async def _start_ki_verarbeitung(self, shareddata: asyncio.Queue):  
            while True:            
                item: KiData = await shareddata.get()
                await self._MoveSchanze(item)
                self.ismoveschanzeaktiv = False

    async def _startasync(self, shareddata: asyncio.Queue, progressring: ft.ProgressRing, zeigebildan, callbackinfos):
        await self._drehe_rad()
        timemulti = 1
        datum = self._erstelle_datum()
        with sessiongen() as session:
            datumid = self._createdatumindb(datum, session)
            for item, image in self.model.loadmodelpytorch(progressring):

                zeigebildan(image)        
                callbackinfos(item) 
                self._verarbeitedaten(item)
                self.currentkidata = item

                if item.laufzeit >= 2 * timemulti:
                    endkidata = self._berechnedurchschnitt(item.laufzeit, item.anzahl, modus=item.erkannter_modus)
                    timemulti += 1
                    self._delete_tmp_data()
                    self._verarbeite_entdaten(endkidata, datumid, session)
                   
                
                    if not self.ismoveschanzeaktiv:
                        await shareddata.put(item)
                        self.ismoveschanzeaktiv = True
               
                await asyncio.sleep(0)
                    
                if not LaufZeitConfig.islaufzeit:
                    self._savetime(self.currentkidata.laufzeit, datumid, session, self.currentkidata.anzahl)
                    break
                            
            

    async def _change_color(self, kidaten: KiData):
        if kidaten.erkannter_modus == Erkanntermodus.FARBE:
            await self.colorchange.setledcolor(kidaten)
    
    async def _MoveSchanze(self, Kidata: KiData):
        if Kidata.erkannter_modus == Erkanntermodus.FARBE and Kidata.label_name != "background":
            await self.schanze.start_changeposition(Kidata)
            await self._change_color(Kidata)
            await self.schanze.start_raddrehen()
    
    def _delete_tmp_data(self):
        KiDataManager.deleteSessionData(SaveDictName.kidatenzwischenspeicher)
        self.kidatenlist.clear()
    
    def _erstelle_datum(self) -> datetime:
        # Pfad zum Ordner "statistikdata" erstellen
        # Pfad zur gewünschten Datei im Ordner "statistikdata" erstellen
        datum = datetime.now()
        #datei_name = datum.strftime("output_%Y-%m-%d_%H-%M-%S.json")
        return datum


    async def _drehe_rad(self):
        await self.schanze.start_raddrehen()

    def _verarbeite_entdaten(self,item: KiData,datumid:int, session: Session):
        if item.label_name.lower() != "background" and int(item.confidence_score) > 1:
            StatistikCreater().savestatistik(item,datumid,session)
        

    def _berechnedurchschnitt(self, laufzeit: float, anzahl: int, modus: str) ->KiData:
        
        daten = KiDataManager.ladeSessiondata(SaveDictName.kidatenzwischenspeicher,List[KiData])   
        
        
        df = pd.DataFrame([vars(data)for data in daten])
        
        result_label_name = df['label_name'].value_counts().idxmax()
        result_confidence_score = df['confidence_score'].mean()
        
        
        return KiData(label_name=result_label_name,anzahl=anzahl,confidence_score=int(result_confidence_score),laufzeit=laufzeit, erkannter_modus=modus)

        

    def _verarbeitedaten(self,item: KiData):
        self.kidatenlist.append(item)
        KiDataManager.saveSessionDaten(SaveDictName.kidatenzwischenspeicher,self.kidatenlist)
    
    def _createdatumindb(self,datum, session: Session):
        return CreateDatumSpeicherung().CreateDatum(session, datum) 
        
    def _savetime(self,laufzeit: float,datumid:int, session: Session,aktuellestueckzahl: int):
        EndStatistik().createzeitdaten(laufzeit,datumid, session,aktuellestueckzahl)