import datetime
from io import TextIOWrapper
import json
from Ki.opencvcode import TrainiertesModel
from shared.shareddata import Shareddata


class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
    
    def start_application(self, e):
        self.dateiname = self._erstelle_speicherdateiname()
        with open(self.dateiname, 'w') as json_file:
            for item in self.model.loadmodel():
                print(item.class_name, item.confidence_score)
                self._verarbeitedaten(item.class_name, json_file)


    def _erstelle_speicherdateiname(self) -> str:
        datei_name = datetime.datetime.now().strftime("output_%Y-%m-%d_%H-%M-%S.json")
        return datei_name

    def _verarbeitedaten(self,class_name, json_file: TextIOWrapper):
        data_to_save = {
            "class_name": class_name,
        }
        
        # Daten in JSON-Format umwandeln
        json_data = json.dumps(data_to_save, indent=2)
        
        # Daten in die offene Datei schreiben
        json_file.write(json_data)
        json_file.write('\n') 
        Shareddata.savedata(class_name)