from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class Auth(Base):
    __tablename__ = 'auth'
    id = Column(String, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(String, primary_key=True)
    business_name = Column(String, nullable=False)
    address = Column(String, nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    owner = Column(String, nullable=False)
