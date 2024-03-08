from modele.InterneDatenModele import KIModelloaderData, KIModelsaverData
import flet as ft
import json

class KiDataManager():
    Pagedata: ft.Page = None
    
    @classmethod
    def classinit(cls,page: ft.Page):
        cls.Pagedata  = page
        
    @classmethod
    def ladeKIDaten(cls) -> KIModelloaderData:
        json_data = cls.Pagedata.session.get("kimodel")
        
        return KIModelloaderData(json_data)