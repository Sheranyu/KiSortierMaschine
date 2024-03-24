
from typing import Any, List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal


class Base(DeclarativeBase):
    pass


class DatumSpeicherung(Base):
    __tablename__ = 'DatumSpeicherung'

    Id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    Datum: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    Statistik: Mapped[List['Statistik']] = relationship('Statistik', back_populates='fremd')
    EndStastik: Mapped[List['EndStastik']] = relationship('EndStastik', back_populates='datumspeicherung')

    def __init__(self,Datum) -> None:
        self.Datum = Datum

class Statistik(Base):
    __tablename__ = 'Statistik'

    Statisik_id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    label_name: Mapped[Optional[str]] = mapped_column(Text)
    confidence_score: Mapped[Optional[int]] = mapped_column(Integer)
    confidence_score_max: Mapped[Optional[int]] = mapped_column(Integer)
    modus: Mapped[Optional[str]] = mapped_column(Text)
    fremd_id: Mapped[Optional[decimal.Decimal]] = mapped_column(ForeignKey('DatumSpeicherung.Id'))

    fremd: Mapped['DatumSpeicherung'] = relationship('DatumSpeicherung', back_populates='Statistik')

    def __init__(self, label_name, confidence_score, modus, confidence_score_max=None, fremd_id= None):
        self.label_name = label_name
        self.confidence_score = confidence_score
        self.modus = modus
        self.fremd_id = fremd_id

class EndStastik(Base):
    __tablename__ = 'EndStastik'

    ZeitID: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    datumspeicherung_id: Mapped[Optional[decimal.Decimal]] = mapped_column(ForeignKey('DatumSpeicherung.Id'))
    laufzeit: Mapped[Optional[float]] = mapped_column(Float)
    stueckzahl: Mapped[Optional[int]] = mapped_column(Integer)

    datumspeicherung: Mapped['DatumSpeicherung'] = relationship('DatumSpeicherung', back_populates='EndStastik')
    def __init__(self, laufzeit: int, datumspeicherung_id: int ,stueckzahl: int):
        pass