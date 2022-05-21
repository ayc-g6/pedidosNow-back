from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    email = Column(String(500), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
