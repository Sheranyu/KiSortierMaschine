
from pydantic import BaseModel, Field


class LaufZeitConfig():
    islaufzeit:bool = False
    istrainingactive: bool = False
    ispauseactive: bool = True

    @classmethod
    def Enable_istrainingactive(cls):
        cls.istrainingactive = True
        
    @classmethod
    def Disable_istrainingactive(cls):
        cls.istrainingactive = False
        
        
class SaveDictName():
    kimodel: str = "kimodel"
    camerasettings: str = "classcreatorsettings"
    kidatenzwischenspeicher: str = "kidatenzwischenspeicher"
    serialsettings: str = "serialsettings"
    topfmodus: str = "topfmodus"
    labellist: str = "labellist"





#!!!!!nicht löschen dient als erinnerung!!!!#


# class ModelDataClass():
#     KiModelpfad = None
#     Modelname = None
#     @classmethod
#     def __init__(cls, KiModelpfad=None,Modelname=None) -> None:
#         cls.KiModelpfad = KiModelpfad
#         cls.Modelname = Modelname
    

# class modelConfig():

#     def __init__(self) -> None:
#         pass
    
#     @classmethod
#     def loadmodelconfig(cls) -> ModelDataClass:
#         try:
#             with open('modelconfig.json', 'r') as file:
#                 daten = json.load(file)
#                 ModelDataClass(daten.KiModelpfad,daten.Modelname)
#         except:
#             print("Fehler beim laden der Datei")
       

#     @classmethod
#     def setconfig(cls):
#         try:
#             with open('modelconfig.json', 'w') as file:
#                 json.dump(ModelDataClass.__dict__, file, indent=4)
#         except:
#             print("Fehler beim laden der Datei")




class settings():
    def loadsettings():
        pass


    def setsettings():
        pass