


from sqlalchemy.orm.session import Session

from db.db_and_models.models import EndStastik


class EndStatistik():
    def createzeitdaten(self,laufzeit: float,aktuellestueckzahl: int,aktulles_datum_id: int ,session: Session):
        modeldata = EndStastik(laufzeit, aktulles_datum_id, aktuellestueckzahl)
        session.add(modeldata)
        session.commit()