import datetime
from io import TextIOWrapper

import flet as ft
from sqlalchemy.orm import Session
from Ki.opencvcode import TrainiertesModel
from configordner.settings import SaveDictName
from db.CRUD.EndStatistik import EndStatistik
from logic.KiDatenManager import KiDataManager
from logic.MoveLogic import SchwanzenBewegungNachFarbe
from modele.InterneDatenModele import Erkanntermodus, KiData
from typing import Any, Generator, List
from datetime import datetime
import pandas as pd

from db.CRUD.Statistik import  StatistikCreater
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.db_and_models.session import sessiongen


class KiDatenVerarbeitung():
    def __init__(self) -> None:
        self.model = TrainiertesModel()
        self.aktuellelaufzeit = None
        self.currentkidata: KiData = None
        self.kidatenlist: List[KiData] = []
        self.schanze = SchwanzenBewegungNachFarbe()
        self.isamdrehen = False
    
    def start_application(self,callback,progressring :ft.ProgressRing) -> Generator[KiData,Any, Any]:
        timemulti = 1
        datum = self._erstelle_datum()
        with sessiongen() as session:
            
            datumid = self._createdatumindb(datum,session)
            for item, image in self.model.loadmodelpytorch(progressring):
                callback(image)
                self.aktuellelaufzeit = item.laufzeit
                
                #print(item.label_name, item.confidence_score)
                yield item
                self._verarbeitedaten(item)
                self.currentkidata = item
                if item.laufzeit >= 1*timemulti:
                     endkidata = self._berechnedurchschnitt(item.laufzeit,item.anzahl, modus=item.erkannter_modus.value)
                     timemulti += 1
                     self.MoveSchanze(item)
                     self._delete_tmp_data()
                     self._verarbeite_entdaten(endkidata,datumid,session)
                     
            self._savetime(self.currentkidata.laufzeit,datumid,session,self.currentkidata.anzahl)

    
    
    def MoveSchanze(self, Kidata: KiData):
        if Kidata.erkannter_modus == Erkanntermodus.FARBE:
            self.schanze.start_changeposition(Kidata)
    
    def _delete_tmp_data(self):
        KiDataManager.deleteSessionData(SaveDictName.kidatenzwischenspeicher)
        self.kidatenlist.clear()
    
    def _erstelle_datum(self) -> datetime:
        # Pfad zum Ordner "statistikdata" erstellen
        # Pfad zur gewünschten Datei im Ordner "statistikdata" erstellen
        datum = datetime.now()
        #datei_name = datum.strftime("output_%Y-%m-%d_%H-%M-%S.json")
        return datum


    def _verarbeite_entdaten(self,item: KiData,datumid:int, session: Session):
        if item.label_name.lower() != "background" and int(item.confidence_score) > 1:
            StatistikCreater().savestatistik(item,datumid,session)

    def _berechnedurchschnitt(self, laufzeit: float, anzahl: int, modus: str) ->KiData:
        
        daten = KiDataManager.ladeSessiondata(SaveDictName.kidatenzwischenspeicher,List[KiData])   
        
        
        df = pd.DataFrame([vars(data)for data in daten])
        
        result_label_name = df['label_name'].value_counts().idxmax()
        result_confidence_score = df['confidence_score'].mean()
        
        
        return KiData(label_name=result_label_name,anzahl=anzahl,confidence_score=int(result_confidence_score),laufzeit=laufzeit, erkannter_modus=modus)

        

    def _verarbeitedaten(self,item: KiData):
        self.kidatenlist.append(item)
        KiDataManager.saveSessionDaten(SaveDictName.kidatenzwischenspeicher,self.kidatenlist)
    
    def _createdatumindb(self,datum, session: Session):
        return CreateDatumSpeicherung().CreateDatum(session, datum) 
        
    def _savetime(self,laufzeit: float,datumid:int, session: Session,aktuellestueckzahl: int):
        EndStatistik().createzeitdaten(laufzeit,datumid, session,aktuellestueckzahl)