from sqlalchemy import Column, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Statistik(Base):
    __tablename__ = 'Statistik'

    id = Column(Integer, primary_key=True)
    class_name = Column(Text)
    confidence_score = Column(Integer)
    def __init__(self, class_name, confidence_score):
        self.class_name = class_name
        self.confidence_score = confidence_score

t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)