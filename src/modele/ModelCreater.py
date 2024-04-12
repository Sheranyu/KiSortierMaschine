

from modele.InterneDatenModele import ErkanntermoduModel, Erkanntermodus

class modelCreatermodus():
    modus: Erkanntermodus
    @classmethod
    def SetErkanntermodus(cls,data:str):
        data = data.strip()
        if data in [mode.value for mode in Erkanntermodus]:
            cls.modus = data
        else:
            print("Ungültiger Modus")

      