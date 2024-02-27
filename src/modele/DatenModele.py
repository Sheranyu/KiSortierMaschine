import numpy as np

class KiData():
    def __init__(self,class_name: str,confidence_score: str) -> None:
        self.class_name = class_name
        self.confidence_score = confidence_score

