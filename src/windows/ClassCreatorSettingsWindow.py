from typing import Self
import flet as ft

#from Designer.design import ClassCreatorDesignPage
from modele.InterneDatenModele import ClassCreatorSettingsModel


class SettingsClassCreator():
    def __new__(self, page: ft.Page) -> Self:
        self.page = page
       
        
        return ft.TextButton("hello world")
    
    def on_change(self, e: ft.ControlEvent):
        modeldata = ClassCreatorSettingsModel(aufnahmeges=e.control.value)
        self.page.client_storage.set("classcreatorsettings", modeldata)
        self.page.update()