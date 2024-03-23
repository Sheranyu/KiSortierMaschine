from pickle import DICT
from typing import Dict, Type, TypeVar
from StatusMeldungen.status import TypeErrorMessages
from configordner.settings import SaveDictName
from modele.InterneDatenModele import KIModelloaderData, KIModelsaverData
import flet as ft
import json

T = TypeVar('T')

class KiDataManager():
    Pagedata: ft.Page = None
    
    @classmethod
    def classinit(cls,page: ft.Page):
        cls.Pagedata  = page
        
    @classmethod
    def ladeKImodel(cls) -> KIModelloaderData:
        json_data = cls.Pagedata.session.get(SaveDictName.kimodel)
        
        return KIModelloaderData(json_data)
    
    @classmethod
    def ladeDaten(cls, dictname: str, typ: Type[T]):
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        json_data = cls.Pagedata.client_storage.get(dictname)
        return typ(**json_data)