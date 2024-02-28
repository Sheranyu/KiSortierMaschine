from typing import List
from db.db_and_models.models import Statistik
from db.db_and_models.session import newsession

class DataCreater():
    def savestatistik(self, daten: Statistik):
        with newsession() as session:
            session.add(daten)
            session.commit()