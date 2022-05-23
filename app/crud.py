from sqlalchemy.orm import Session
import uuid

import models, schemas

def get_auth_by_email(db: Session, email: str):
    return db.query(models.Auth).filter(models.Auth.email == email).first()

def get_auths(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Auth).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.AuthCustomerCreate):
    hashed_password = customer.password # TODO Hash password
    auth_id = str(uuid.uuid4())
    db_auth = models.Auth(id=auth_id, email=customer.email, hashed_password=hashed_password)
    db_customer = models.Customer(id=auth_id, username=customer.username)
    db.add(db_auth)
    db.add(db_customer)
    db.commit()
    return db_auth

def create_business(db: Session, business: schemas.AuthBusinessCreate):
    hashed_password = business.password # TODO Hash password
    auth_id = str(uuid.uuid4())
    db_auth = models.Auth(id=auth_id, email=business.email, hashed_password=hashed_password)
    db_customer = models.Business(id=auth_id, business_name=business.business_name, address=business.address)
    db.add(db_auth)
    db.add(db_customer)
    db.commit()
    return db_auth

def create_product(db: Session, product: schemas.ProductBase):
    # hashed_password = business.password # TODO Hash password
    # auth_id = str(uuid.uuid4())
    # db_auth = models.Auth(id=auth_id, email=business.email, hashed_password=hashed_password)
    # product_id = str(uuid.uuid4())
    db_product = models.Product(name=product.name, price=product.price, owner=product.owner)
    # db.add(db_auth)
    db.add(db_product)
    db.commit()
    return db_product