


from sqlalchemy.orm.session import Session

from db.db_and_models.models import EndStastik


class EndStatistik():
    def createzeitdaten(self,laufzeit: float,aktuellestueckzahl: int,aktulles_datum_id: int ,session: Session):
        print("im speichern")
        print(laufzeit)
        print(aktuellestueckzahl)
        print(aktulles_datum_id)
        modeldata = EndStastik( aktulles_datum_id,laufzeit, aktuellestueckzahl)
        session.add(modeldata)
        session.commit()
            
        print("angekommen")