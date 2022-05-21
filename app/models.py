from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Authentication(Base):
    __tablename__ = 'authentication'
    id = Column(String(500), primaryKey=True)
    email = Column(String(500), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)


