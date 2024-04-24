




from typing import Tuple
from sqlalchemy import Row, Sequence
from db.CRUD.DatumSpeicherung import ReadDatumSpeicherung
from db.CRUD.EndStatistik import EndStatistik
from db.CRUD.Statistik import StatistikReader
from db.db_and_models.models import Statistik
from db.db_and_models.session import sessiongen

class KIStatistikLoader():
    def __init__(self) -> None:
        pass
    def loaddatum(self):
        with sessiongen() as session:
            result = ReadDatumSpeicherung().ReadDatum(session)
            
            return result
        
    def loadstatistik(self,id: int):
        with sessiongen() as session:
            result = StatistikReader().Readdata(id,session)
            return result
        
    def loadendstatistik(self,id: int):
        with sessiongen() as session:
            result = EndStatistik().getStatistik(id,session)
            return result