
import flet as ft

#from Designer.design import ClassCreatorDesignPage
from Designer.design import ClassCreatorDesignPage
from configordner.settings import SaveDictName
from lib.Components import BPSSlider
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import CameraSettingsModel




class SettingsClassCreator(ft.Column):
    
    def __init__(self) -> None:
        super().__init__()

    def build(self):   
        self.endcolum = BPSSlider()
        return self.endcolum

    
    # def on_change(self, e: ft.ControlEvent):
    #     self.aufnahmegestextausgabe.value = f"{e.control.value} BPS"
    #     modeldata = CameraSettingsModel(aufnahmeges=int(e.control.value))
    #     #self.aufnahmegestext.value += str(e.control.value)
    #     self.page.client_storage.set(SaveDictName.camerasettings, modeldata)  
    #     self.update()
        
    # def did_mount(self):
    #     if self.page.client_storage.get(SaveDictName.camerasettings):
            
    #         data = KiDataManager.ladeDaten(SaveDictName.camerasettings,CameraSettingsModel)
    #         self.aufnahmeges.value = data.aufnahmeges
    #         self.aufnahmegestextausgabe.value = f"{data.aufnahmeges} BPS"
    #         self.update()