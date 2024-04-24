

import datetime
from db.db_and_models.models import DatumSpeicherung
from sqlalchemy.orm.session import Session
from sqlalchemy import asc, desc, insert, select

class CreateDatumSpeicherung():
    def CreateDatum(self,session: Session, gesuchtes_datum: datetime) -> int:
        insertdata = insert(DatumSpeicherung).values(Datum=gesuchtes_datum).returning(DatumSpeicherung)
        result = session.execute(insertdata).scalar()
        session.commit()
        return result.Id

class UpdatedatumSpeicherung():
    pass

class ReadDatumSpeicherung():
    def ReadDatum(self,session: Session):
        result = session.execute(select(DatumSpeicherung).order_by(DatumSpeicherung.Datum)).scalars()
        
        return result.fetchall()
            
        