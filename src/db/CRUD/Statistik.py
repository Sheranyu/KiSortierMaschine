import datetime
from typing import List
from sqlalchemy import select, insert
from db.db_and_models.models import Statistik, DatumSpeicherung
from sqlalchemy.orm.session import Session
from db.db_and_models.session import sessiongen
from modele.InterneDatenModele import KiData

class StatistikCreater():
    def savestatistik(self,daten: KiData,aktulles_datum_id: int ,session: Session):
        print(daten)
        modeldata = Statistik(label_name=daten.label_name,
                              confidence_score=daten.confidence_score,
                              modus=daten.erkannter_modus.value, fremd_id=aktulles_datum_id,
                              confidence_score_max=daten.confidence_score_max)

        session.add(modeldata)
        session.commit()

class StatistikReader():
    def Readdata():
        with sessiongen() as session:
            statisiken: List[Statistik] = session.query(Statistik).all()
            for item in statisiken:
                print(item.confidence_score , item.class_name)


class UpdateStatistik():
    def UpdateData():
        pass