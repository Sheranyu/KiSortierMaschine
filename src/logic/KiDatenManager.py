

from typing import Type, TypeVar
from StatusMeldungen.status import TypeErrorMessages
from configordner.settings import SaveDictName
from modele.InterneDatenModele import KIModelloaderData
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
            if json_data is None:
                return typ()
            
            expected_attributes = set(typ.__annotations__.keys())
            json_attributes = set(json_data.keys())
            if expected_attributes != json_attributes:
                raise TypeError("JSON data does not match the expected type")
        except:
            return typ()

        return typ(**json_data)
    
    @classmethod
    def ladeSessiondata(cls, dictname: str, typ: Type[T]):
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        try:
            json_data = cls.Pagedata.session.get(dictname)  
            if json_data is None:
                return typ()
            if isinstance(json_data, dict):
                expected_attributes = set(typ.__annotations__.keys())
                json_attributes = set(json_data.keys())
                if expected_attributes != json_attributes:
                    raise TypeError("JSON data does not match the expected type")
                #alte möglichkeit um datne in pydantic zu passen geht soweit gut solange keine liste im modle ist
                return typ(**json_data)
            else:
                
                # "model_validate" funktioniert auch mit listen im pydantic models/bessere und weniger fehler anfälliger weg
                return typ.model_validate(json_data)
        except Exception as e:
            print("Exception occurred:", e)
            return typ()
        
        
    
    
    
    @classmethod
    def ladelistSessiondata(cls, dictname: str, typ: Type[T]) -> T:
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
    def saveclientdata(cls,dictname, data: dict):
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        
        cls.Pagedata.client_storage.set(dictname,data)
    
    @classmethod
    def saveSessionDaten(cls,dictname: str, data: dict):
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        
        cls.Pagedata.session.set(dictname,data)
        
    @classmethod
    def deleteSessionData(cls,dictname: str):
        if not isinstance(dictname, str):
            raise TypeError(TypeErrorMessages.DICT_IS_NO_STRING)
        cls.Pagedata.session.remove(dictname)