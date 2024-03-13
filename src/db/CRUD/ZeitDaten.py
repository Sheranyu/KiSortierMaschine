


from sqlalchemy.orm.session import Session

from db.db_and_models.models import ZeitDaten


class zeitdaten():
    def createzeitdaten(self,laufzeit: float,aktulles_datum_id: int ,session: Session):
        modeldata = ZeitDaten(laufzeit, aktulles_datum_id)
        session.add(modeldata)
        session.commit()