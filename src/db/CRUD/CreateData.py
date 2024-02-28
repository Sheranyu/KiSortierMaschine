import datetime
from typing import List
from sqlalchemy import select
from db.db_and_models.models import Statistik, DatumSpeicherung
from sqlalchemy.orm.session import Session
from db.db_and_models.session import newsession
from modele.InterneDatenModele import KiData

class DataCreater():
    def savestatistik(daten: KiData,gesuchtes_datum: datetime ,session: Session):
        modeldata = Statistik(class_name=daten.class_name,
                              confidence_score=daten.confidence_score,
                              erkannte_farbe=daten.erkannte_farbe,
                              erkannte_form=daten.erkannte_form)
        
        aktuellesdatenobject = select(DatumSpeicherung).where(DatumSpeicherung.Datum == gesuchtes_datum)
        result = session.execute(aktuellesdatenobject).first()



        session.add(daten)
        session.commit()

    