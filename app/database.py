from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

POSTGRE_SQL_URL = os.getenv('DATABASE_URL')
print(POSTGRE_SQL_URL)
engine = create_engine(POSTGRE_SQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
