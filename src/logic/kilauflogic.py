import datetime
from io import TextIOWrapper

import flet as ft
from sqlalchemy.orm import Session
from Ki.opencvcode import TrainiertesModel
from configordner.settings import SaveDictName
from db.CRUD.EndStatistik import EndStatistik
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import KiData
from typing import Any, Generator, List
from datetime import datetime


from db.CRUD.Statistik import  StatistikCreater
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.db_and_models.session import sessiongen


class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.aktuellelaufzeit = None
        self.kidaten: KiData = None
        self.kidatenlist: List[KiData] = []
    
    def start_application(self,callback,progressring :ft.ProgressRing) -> Generator[KiData,Any, Any]:
        timemulti = 1
        datum = self._erstelle_datum()
        with sessiongen() as session:
            
            datumid = self._createdatumindb(datum,session)
            for item, image in self.model.loadmodelpytorch(progressring):
                callback(image)
                self.aktuellelaufzeit = item.laufzeit
                #print(item.label_name, item.confidence_score)
                yield item
                self._verarbeitedaten(item)
                self.kidaten = item
                if item.laufzeit >= 1*timemulti:
                     self._berechnedurchschnitt()
                     timemulti += 1
                     
            self._savetime(self.kidaten.laufzeit,datumid,session,self.kidaten.anzahl)

    
    def _delete_tmp_data(self):
        KiDataManager.deleteSessionData(SaveDictName.kidatenzwischenspeicher)
    
    def _erstelle_datum(self) -> datetime:
        # Pfad zum Ordner "statistikdata" erstellen
        # Pfad zur gewünschten Datei im Ordner "statistikdata" erstellen
        datum = datetime.now()
        #datei_name = datum.strftime("output_%Y-%m-%d_%H-%M-%S.json")
        return datum


    def _verarbeite_entdaten(self,item: KiData,datumid:int, session: Session):
        if item.label_name.lower() != "background" and int(item.confidence_score) > 1:
            StatistikCreater().savestatistik(item,datumid,session)

    def _berechnedurchschnitt(self) ->KiData:
        print("data")
        daten = KiDataManager.ladeSessiondata(SaveDictName.kidatenzwischenspeicher,List[KiData])   
        print(daten)
        

    def _verarbeitedaten(self,item: KiData):
        self.kidatenlist.append(item)
        KiDataManager.saveSessionDaten(SaveDictName.kidatenzwischenspeicher,self.kidatenlist)
    
    def _createdatumindb(self,datum, session: Session):
        return CreateDatumSpeicherung().CreateDatum(session, datum) 
        
    def _savetime(self,laufzeit: float,datumid:int, session: Session,aktuellestueckzahl: int):
        EndStatistik().createzeitdaten(laufzeit,datumid, session,aktuellestueckzahl)