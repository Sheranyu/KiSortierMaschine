

class KiData():
    def __init__(self, class_name, confidence_score, erkannte_farbe = None, erkannte_form=None):
        self.class_name = class_name
        self.confidence_score = confidence_score
        self.erkannte_farbe = erkannte_farbe
        self.erkannte_form = erkannte_form

