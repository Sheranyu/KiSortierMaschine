
from ast import List
from typing import Dict, Type, TypeVar
from StatusMeldungen.status import TypeErrorMessages
from configordner.settings import SaveDictName
from modele.InterneDatenModele import KIModelloaderData, KIModelsaverData
import flet as ft

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
        try:
            json_data = cls.Pagedata.client_storage.get(dictname)
        except:
            raise ValueError("No data found for the given dictname")

        return typ(**json_data)
    
    
    @classmethod
    def ladeSessiondata(cls, dictname: str, typ: Type[T]) -> T:
        itemlist: typ = []
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        json_data = cls.Pagedata.session.get(dictname)
        
        
        if json_data is None:
            raise ValueError("No data found for the given dictname")
        if not isinstance(json_data, list):
            raise ValueError("Data retrieved is not in list format")
        
        
        itemlist.extend(json_data)
        
        return itemlist

    
    @classmethod
    def saveSessionDaten(cls,dictname: str, data: Dict):
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        
        cls.Pagedata.session.set(dictname,data)
        
    @classmethod
    def deleteSessionData(cls,dictname: str):
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        cls.Pagedata.session.remove(dictname)