

import datetime
from db.db_and_models.models import DatumSpeicherung
from sqlalchemy.orm.session import Session
from sqlalchemy import insert

class CreateDatumSpeicherung():
    def CreateDatum(self,session: Session, gesuchtes_datum: datetime) -> int:
        insertdata = insert(DatumSpeicherung).values(Datum=gesuchtes_datum).returning(DatumSpeicherung)
        result = session.execute(insertdata).scalar()
        session.commit()
        return result.Id

class UpdatedatumSpeicherung():
    pass