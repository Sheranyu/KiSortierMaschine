

from modele.InterneDatenModele import ErkanntermoduModel, Erkanntermodus

class modelCreatermodus():
    modus: Erkanntermodus
    @classmethod
    def SetErkanntermodus(cls,data:str):
        data = data.strip()
        if Erkanntermodus.FARBE.value == data:
            modelCreatermodus.SetErkanntermodus(Erkanntermodus.FARBE)
        if Erkanntermodus.FORM.value == data:
            modelCreatermodus.SetErkanntermodus(Erkanntermodus.FORM)
    

      