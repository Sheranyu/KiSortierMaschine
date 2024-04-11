


from enum import Enum
from typing import Any, Optional, Union
from pydantic import BaseModel, ConfigDict, Field
import cv2
import flet as ft

class ModelTyp(Enum):
    KERAS = "keras"
    ONNX = "onnx"
    TORCH = "torch"
    
class Erkanntermodus(Enum):
    FARBE = "farbmodus"
    FORM = "Formmodus"


class SchanzenSteuerungFarbe(Enum):
    ROT = "rot"
    GREEN = "green"
    BLUE = "blue"
    SONSTIGES = "sonstiges"
    BACKGROUND = "background"
 
 



class LeuchtFarbenLampe(Enum):
    ROT = "rot"
    GRUEN = "gruen"
    BLAU = "blau"
    BACKGROUND = ""
    LILA = "lila"
    WEISS = "weiss"
    SCHWARZ = "schwarz"
    GELB = "gelb"
    SONSTIGES = "sonstiges"   


class ErkanntermoduModel(BaseModel):
    modus: Optional[Erkanntermodus]
    


class KiData(BaseModel):
    label_name: str
    confidence_score: int
    erkannter_modus: Optional[Union[Erkanntermodus, str]] = Field(default=None)
    laufzeit: float
    confidence_score_max: Optional[int] = Field(default=None)
    anzahl: int
    

 
class KIModelsaverData():
    def __init__(self,ModelName=None, pfad_model=None,label_datei_name=None,pfad_label=None, modeltyp = ModelTyp.KERAS.value) -> None:
      
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
    model_config = ConfigDict(extra='ignore',arbitrary_types_allowed=False)
    imagedata: Any
    aufnahmefotoname: str
   
        
        
class CameraSettings(BaseModel):
    aufnahmeges: int = Field(default=10)
    Camera: int = Field(default=0)

class SerialConfig(BaseModel):
    COM: str = Field(default="COM5")
    

class KiModeltrainingConfigdata(BaseModel):
    bachsize: int
    epoches: int
    lernrate: float
    maxdatenseatze: int
    
    
    

    
    
