

from typing import List
from db.db_and_models.models import Statistik
from db.db_and_models.session import newsession

class Datenverteiler():

    def savestatistik(self, daten: Statistik):
        with newsession() as session:
            session.add(daten)
            session.commit()
        
    def loadstatistik(self):
        with newsession() as session:
            statisiken: List[Statistik] = session.query(Statistik).all()
            for item in statisiken:
                print(item.id, item.class_name)
            