
from typing import List, Sequence, Tuple
from db.db_and_models.models import Statistik, DatumSpeicherung
from sqlalchemy.orm.session import Session
from db.db_and_models.session import sessiongen
from modele.InterneDatenModele import KiData
from sqlalchemy import Row, select
class StatistikCreater():
    def savestatistik(self,daten: KiData,aktulles_datum_id: int ,session: Session):
        
        modeldata = Statistik(label_name=daten.label_name,
                              confidence_score=daten.confidence_score,
                              modus=daten.erkannter_modus.value, fremd_id=aktulles_datum_id,
                              confidence_score_max=daten.confidence_score_max)

        session.add(modeldata)
        session.commit()

class StatistikReader():
    def Readdata(self,datum_id: int,session: Session):
        smt = select(Statistik).where(Statistik.fremd_id == datum_id).order_by()
        result = session.execute(smt).scalars()
       
        
        return result.fetchall()


class UpdateStatistik():
    def UpdateData():
        pass