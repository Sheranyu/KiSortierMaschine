import datetime
from io import TextIOWrapper
import json
import os
import time

from sqlalchemy.orm import Session
from Ki.opencvcode import TrainiertesModel
from db.db_and_models.models import DatumSpeicherung
from modele.InterneDatenModele import KiData
from typing import List, Tuple
from jsonconverter.converter import converttoJson
from pathlib import Path
from datetime import datetime


from db.CRUD.Statistik import  StatistikCreater
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.db_and_models.session import newsession


class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.data_to_save: List[KiData] = []
    
    def start_application(self):
        datum = self._erstelle_speicherdateiname()
        with newsession() as session:
            datumid = self._createdatum(datum,session)
            for item in self.model.loadmodel():
                print(item.class_name, item.confidence_score)
                self._verarbeitedaten(item,datumid,session)

        

    def _erstelle_speicherdateiname(self) -> Tuple[str, datetime]:
        # Pfad zum Ordner "statistikdata" erstellen
        # Pfad zur gewünschten Datei im Ordner "statistikdata" erstellen
        datum = datetime.now()
        #datei_name = datum.strftime("output_%Y-%m-%d_%H-%M-%S.json")

        return datum

    def _verarbeitedaten(self,item: KiData,datumid:int, session: Session):
        StatistikCreater().savestatistik(item,datumid,session)
    
    def _createdatum(self,datum, session: Session):
         return CreateDatumSpeicherung().CreateDatum(session, datum) 
        
        