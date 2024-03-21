
import flet as ft

#from Designer.design import ClassCreatorDesignPage
from Designer.design import ClassCreatorDesignPage
from modele.InterneDatenModele import ClassCreatorSettingsModel




class SettingsClassCreator(ClassCreatorDesignPage):
    
    def __init__(self) -> None:
        super().__init__()
        
    def build(self):   
        self.columincontainer = ft.Column([self.aufnahmegestext,ft.Container(self.aufnahmeges)])
        self.endcolum = ft.Column([ft.Container(self.columincontainer)])   
        return self.endcolum

    
    def on_change(self, e: ft.ControlEvent):
    
        modeldata = ClassCreatorSettingsModel(aufnahmeges=int(e.control.value))
        #self.aufnahmegestext.value += str(e.control.value)
        self.update()
        return
        self.page.client_storage.set("classcreatorsettings", modeldata)
        self.page.update()
        
    