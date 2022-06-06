from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float, func
from sqlalchemy.orm import relationship
from typing import Optional

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

class Delivery(Base):
    __tablename__ = 'deliveries'
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(String, primary_key=True)
    business_name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    class Config:
        orm_mode = True

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description= Column(String, nullable= False)
    price = Column(Float, nullable=False)
    owner = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)

    class Config:
        orm_mode = True

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    customer_id = Column(String, nullable=False)
    business_id = Column(String, nullable=False)
    product_id = Column(Integer, nullable=False)
    delivery_address = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)

    class Config:
        orm_mode = True

class OrderDelivery(Base):
    order_id = Column(Integer, primary_key=True)
    delivery_id = Column(String, nullable=False)

    class Config:
        orm_mode = True