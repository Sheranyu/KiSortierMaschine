


from enum import Enum
from typing import Any


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
        
class KIModel():
    def __init__(self,ModelName=None, pfad_model=None,label_name=None,pfad_label=None, modeltyp = ModelTyp.KERAS.value) -> None:
        self.ModelName = ModelName
        self.label_name = label_name
        self.pfad_model = pfad_model
        self.pfad_label = pfad_label
        self.modeltyp = modeltyp

class KiClassList():
    def __init__(self,index:int,classname:str,speicherpfad:str) -> None:
        self.index = index
        self.classname = classname
        self.speicherpfad = speicherpfad

    