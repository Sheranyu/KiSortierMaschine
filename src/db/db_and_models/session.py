
from sqlalchemy.orm import sessionmaker
from db.db_and_models.engine import engine




sessiongen = sessionmaker(engine)