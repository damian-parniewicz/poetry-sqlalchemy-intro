from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)

Session = sessionmaker(engine)

Base = declarative_base()


def create_tables() -> None:
    Base.metadata.create_all(engine)
