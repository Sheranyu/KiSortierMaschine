import datetime
from io import TextIOWrapper
import json
import os
import time
from Ki.opencvcode import TrainiertesModel
from modele.InterneDatenModele import KiData
from typing import List
from jsonconverter.converter import converttoJson
from pathlib import Path
from datetime import datetime


from db.CRUD.CreateData import  DataCreater
from db.db_and_models.session import newsession


class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.data_to_save: List[KiData] = []
    
    def start_application(self):
        self.dateiname = self._erstelle_speicherdateiname()
        with newsession() as session:
            for item in self.model.loadmodel():
                print(item.class_name, item.confidence_score)
                self._verarbeitedaten(item)

        

    def _erstelle_speicherdateiname(self) -> str:
        # Pfad zum Ordner "statistikdata" erstellen
        # Pfad zur gewünschten Datei im Ordner "statistikdata" erstellen
        datei_name = datetime.now().strftime("output_%Y-%m-%d_%H-%M-%S.json")

        return datei_name

    def _verarbeitedaten(self,item: KiData, json_file: TextIOWrapper):
        DataCreater().savestatistik(item)
       
        
        
        