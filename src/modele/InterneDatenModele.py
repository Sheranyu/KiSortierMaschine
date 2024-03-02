


from enum import Enum


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
    def __init__(self,ModelName, pfad, modeltyp = ModelTyp.KERAS.value) -> None:
        self.ModelName = ModelName
        self.pfad = pfad
        self.modeltyp = modeltyp
