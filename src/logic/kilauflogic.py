import datetime
from io import TextIOWrapper

import flet as ft
from sqlalchemy.orm import Session
from Ki.opencvcode import TrainiertesModel
from db.CRUD.EndStatistik import EndStatistik
from modele.InterneDatenModele import KiData
from typing import Any, Generator
from datetime import datetime


from db.CRUD.Statistik import  StatistikCreater
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.db_and_models.session import sessiongen


class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.aktuellelaufzeit = None
        self.kidaten = KiData()
    
    def start_application(self,callback,progressring :ft.ProgressRing) -> Generator[KiData,Any, Any]:
        datum = self._erstelle_datum()
        with sessiongen() as session:
            
            datumid = self._createdatumindb(datum,session)
            for item, image in self.model.loadmodelpytorch(progressring):
                callback(image)
                self.aktuellelaufzeit = item.laufzeit
                #print(item.label_name, item.confidence_score)
                yield item
                self._verarbeitedaten(item,datumid,session)
                self.kidaten = item
            self._savetime(self.kidaten.laufzeit,datumid,session,self.kidaten.anzahl)

    def _erstelle_datum(self) -> datetime:
        # Pfad zum Ordner "statistikdata" erstellen
        # Pfad zur gewünschten Datei im Ordner "statistikdata" erstellen
        datum = datetime.now()
        #datei_name = datum.strftime("output_%Y-%m-%d_%H-%M-%S.json")
        return datum
    
    def getvideodata():
        pass

    def _verarbeitedaten(self,item: KiData,datumid:int, session: Session):
        if item.label_name.lower() != "background" and int(item.confidence_score) > 1:
            StatistikCreater().savestatistik(item,datumid,session)
    
    def _createdatumindb(self,datum, session: Session):
        return CreateDatumSpeicherung().CreateDatum(session, datum) 
        
    def _savetime(self,laufzeit: float,datumid:int, session: Session,aktuellestueckzahl: int):
        EndStatistik().createzeitdaten(laufzeit,datumid, session,aktuellestueckzahl)