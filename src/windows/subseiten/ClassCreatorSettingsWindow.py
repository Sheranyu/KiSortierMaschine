
import flet as ft

#from Designer.design import ClassCreatorDesignPage
from Designer.design import ClassCreatorDesignPage
from configordner.settings import SaveDictName
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import ClassCreatorSettingsModel




class SettingsClassCreator(ClassCreatorDesignPage):
    
    def __init__(self) -> None:
        super().__init__()

    def build(self):   
        self.textausgabeBPS = ft.Container(self.aufnahmegestextausgabe,alignment=ft.alignment.center)
        self.columincontainer = ft.Column([self.aufnahmegestext,self.aufnahmeges,self.textausgabeBPS])
        self.endcolum = ft.Column([ft.Container(self.columincontainer)])   
        return self.endcolum

    
    def on_change(self, e: ft.ControlEvent):
        self.aufnahmegestextausgabe.value = f"{e.control.value} BPS"
        modeldata = ClassCreatorSettingsModel(aufnahmeges=int(e.control.value))
        #self.aufnahmegestext.value += str(e.control.value)
        self.page.client_storage.set(SaveDictName.classcreatorsettings, modeldata)  
        self.update()
        
    def did_mount(self):
        if self.page.client_storage.get(SaveDictName.classcreatorsettings):
            
            data = KiDataManager.ladeDaten(SaveDictName.classcreatorsettings,ClassCreatorSettingsModel)
            self.aufnahmeges.value = data.aufnahmeges
            self.aufnahmegestextausgabe.value = f"{data.aufnahmeges} BPS"
            self.update()