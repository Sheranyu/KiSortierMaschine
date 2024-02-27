import datetime
from io import TextIOWrapper
import json
import os
import time
from Ki.opencvcode import TrainiertesModel
from modele.DatenModele import KiData
from typing import List
from jsonconverter.converter import converttoJson
from pathlib import Path
from datetime import datetime
class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.data_to_save: List[KiData] = []
    
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

    def _verarbeitedaten(self,item: List[KiData], json_file: TextIOWrapper):
        self.data_to_save.append(item)
       # self.jsondata = converttoJson(self.data_to_save)
        
        json_file.seek(0) 
        data = json.dumps([vars(data) for data in self.data_to_save], indent=2)
        json_file.write(data) # Setzt den Dateizeiger an den Anfang der Datei
        #json_file.write(self.data_to_save)
        #json.dump(self.data_to_save,json_file,indent=2)
        # Daten in JSON-Format umwandeln
       
        
        
        