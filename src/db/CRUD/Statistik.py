import datetime
from typing import List
from sqlalchemy import select, insert
from db.db_and_models.models import Statistik, DatumSpeicherung
from sqlalchemy.orm.session import Session
from db.db_and_models.session import newsession
from modele.InterneDatenModele import KiData

class StatistikCreater():
    def savestatistik(self,daten: KiData,gesuchtes_datum: datetime ,session: Session):
        modeldata = Statistik(class_name=daten.class_name,
                              confidence_score=daten.confidence_score,
                              erkannte_farbe=daten.erkannte_farbe,
                              erkannte_form=daten.erkannte_form)
        
        aktuellesdatenobject = select(DatumSpeicherung).where(DatumSpeicherung.Datum == gesuchtes_datum)
        result = session.execute(aktuellesdatenobject).scalar()
        
        
        if result is None:
            insertdata = insert(DatumSpeicherung).values(Datum=gesuchtes_datum).returning(DatumSpeicherung)
            result = session.execute(insertdata).scalar()
            
            session.commit()
            
        
        modeldata.fremd_id = result.Id

        session.add(modeldata)
        session.commit()

class StatistikReader():
    def Readdata():
        with newsession() as session:
            statisiken: List[Statistik] = session.query(Statistik).all()
            for item in statisiken:
                print(item.confidence_score , item.class_name)


class UpdateStatistik():
    def UpdateData():
        pass