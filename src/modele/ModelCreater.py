

from modele.InterneDatenModele import ErkanntermoduModel, Erkanntermodus

class modelCreatermodus():
    modus: Erkanntermodus
    @classmethod
    def SetErkanntermodus(cls,data:str):
        data = data.strip()
        cls.modus = Erkanntermodus(data)
        

      