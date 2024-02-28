
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Text
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

    def __init__(self,Datum) -> None:
        self.Datum = Datum

class Statistik(Base):
    __tablename__ = 'Statistik'

    Statisik_id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    class_name: Mapped[Optional[str]] = mapped_column(Text)
    confidence_score: Mapped[Optional[int]] = mapped_column(Integer)
    erkannte_farbe: Mapped[Optional[str]] = mapped_column(Text)
    erkannte_form: Mapped[Optional[str]] = mapped_column(Text)
    fremd_id: Mapped[Optional[decimal.Decimal]] = mapped_column(ForeignKey('DatumSpeicherung.Id'))

    fremd: Mapped['DatumSpeicherung'] = relationship('DatumSpeicherung', back_populates='Statistik')

    def __init__(self, class_name, confidence_score, erkannte_farbe, erkannte_form, fremd_id):
        self.class_name = class_name
        self.confidence_score = confidence_score
        self.erkannte_farbe = erkannte_farbe
        self.erkannte_form = erkannte_form
        self.fremd_id = fremd_id

