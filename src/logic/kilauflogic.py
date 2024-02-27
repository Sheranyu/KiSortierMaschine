import datetime
from io import TextIOWrapper
import json
import os
import time
from Ki.opencvcode import TrainiertesModel
from modele.DatenModele import KiData
from shared.shareddata import Shareddata
from typing import List
from jsonconverter.converter import converttoJson
from pathlib import Path
from datetime import datetime
class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.data_to_save: dict[List] = {"data" : []}
    
    def start_application(self):
        self.dateiname = self._erstelle_speicherdateiname()
        with open(self.dateiname, 'w') as json_file:
            for item in self.model.loadmodel():
                print(item.class_name, item.confidence_score)
                self._verarbeitedaten(item, json_file)
                time.sleep(0.2)
        

    def _erstelle_speicherdateiname(self) -> str:
        # Pfad zum Ordner "statistikdata" erstellen
        ordner_c_pfad = Path(__file__).resolve().parent.parent / "statistikdata"
        # Pfad zur gewünschten Datei im Ordner "statistikdata" erstellen
        datei_name = datetime.now().strftime("output_%Y-%m-%d_%H-%M-%S.json")
        Kidatei = ordner_c_pfad / datei_name

        return Kidatei

    def _verarbeitedaten(self,item: KiData, json_file: TextIOWrapper):
        self.jsondata = converttoJson(item)
        self.data_to_save["data"].append(self.jsondata)
        json_file.seek(0)  # Setzt den Dateizeiger an den Anfang der Datei
        json_file.truncate() 
        json.dump(self.data_to_save,json_file,indent=2)
        # Daten in JSON-Format umwandeln
       
        
        
        