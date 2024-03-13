


from enum import Enum
from typing import Any
from pydantic import BaseModel
import cv2


class ModelTyp(Enum):
    KERAS = "keras"
    ONNX = "onnx"
    TORCH = "torch"



class KiData():
    def __init__(self, label_name, confidence_score ,erkannter_modus,confidence_score_max= None):
        self.label_name = label_name
        self.confidence_score = confidence_score
        self.erkannter_modus = erkannter_modus
        self.confidence_score_max = confidence_score_max
        
class KIModelsaverData():
    def __init__(self,ModelName=None, pfad_model=None,label_datei_name=None,pfad_label=None, modeltyp = ModelTyp.KERAS) -> None:
      
        self.ModelName = ModelName
        self.label_datei_name = label_datei_name
        self.pfad_model = pfad_model
        self.pfad_label = pfad_label
        self.modeltyp = modeltyp
        
class KIModelloaderData():
    def __init__(self, data = None) -> None:
        if data is not None:
            self.ModelName = data["ModelName"]
            self.label_datei_name = data["label_datei_name"]
            self.pfad_model = data["pfad_model"]
            self.pfad_label = data["pfad_label"]
            self.modeltyp = data["modeltyp"]

class KiClassList():
    def __init__(self,index:int,classname:str,speicherpfad:str) -> None:
        self.index = index
        self.classname = classname
        self.speicherpfad = speicherpfad
        
#hier kommt pydantic zum einsatz pydandic prüft ob die typen wirklich passen
class AufnahmeDaten(BaseModel):
    imagedata: cv2.typing.MatLike
    aufnahmefotoname: str
    class Config:
        arbitrary_types_allowed = True
    
    