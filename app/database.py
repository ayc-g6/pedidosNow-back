from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRE_SQL_URL = "postgre://localhost:5432/pedidosYa"
engine = create_engine(POSTGRE_SQL_URL)
Base = declarative_base()
