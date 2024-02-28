

from typing import List
from db.db_and_models.models import Statistik
from db.db_and_models.session import newsession

class DataReader():

        
    def loadstatistik(self):
        with newsession() as session:
            statisiken: List[Statistik] = session.query(Statistik).all()
            for item in statisiken:
                print(item.confidence_score , item.class_name)
            