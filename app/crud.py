from sqlalchemy.orm import Session
import uuid

import models, schemas

PRODUCTS_PER_PAGE = 5

def delete_database(db: Session):
    db.query(models.Auth).delete()
    db.query(models.Customer).delete()
    db.query(models.Business).delete()
    db.query(models.Delivery).delete()
    db.commit()

def delete_database_products(db: Session):
    db.query(models.Product).delete()
    db.commit()

def get_auth_by_email(db: Session, email: str):
    return db.query(models.Auth).filter(models.Auth.email == email).first()

def get_auths(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Auth).offset(skip).limit(limit).all()

def is_business(db: Session, id: str):
    return bool(db.query(models.Business).filter(models.Business.id == id).first())

def is_customer(db: Session, id: str):
    return bool(db.query(models.Customer).filter(models.Customer.id == id).first())

def is_delivery(db: Session, id: str):
    return bool(db.query(models.Delivery).filter(models.Delivery.id == id).first())

def create_delivery(db: Session, delivery: schemas.AuthDeliveryCreationRequest):
    auth_id = str(uuid.uuid4())
    db_auth = models.Auth(id=auth_id, email=delivery.email, hashed_password=delivery.password)
    db_delivery = models.Delivery(id=auth_id, username=delivery.username)
    db.add(db_auth)
    db.add(db_delivery)
    db.commit()
    return schemas.AuthDeliveryCreationResponse(id=auth_id, username=delivery.username, email=delivery.email)

def create_customer(db: Session, customer: schemas.AuthCustomerCreationRequest):
    auth_id = str(uuid.uuid4())
    db_auth = models.Auth(id=auth_id, email=customer.email, hashed_password=customer.password)
    db_customer = models.Customer(id=auth_id, username=customer.username)
    db.add(db_auth)
    db.add(db_customer)
    db.commit()
    return schemas.AuthCustomerCreationResponse(id=auth_id, username=customer.username, email=customer.email)

def create_business(db: Session, business: schemas.AuthBusinessCreationRequest):
    hashed_password = business.password # TODO Hash password
    auth_id = str(uuid.uuid4())
    db_auth = models.Auth(id=auth_id, email=business.email, hashed_password=hashed_password)
    db_customer = models.Business(id=auth_id, business_name=business.business_name, address=business.address)
    db.add(db_auth)
    db.add(db_customer)
    db.commit()
    return schemas.AuthBusinessCreationResponse(id=auth_id, business_name=business.business_name, email=business.email, address=business.address)

def get_business(db: Session, business_id: str):
    return db.query(models.Business).filter(models.Business.id == business_id).first()

def create_product(db: Session, product: schemas.ProductBase, owner_id: str):
    db_product = models.Product(name=product.name, price=product.price, owner=owner_id, calories=product.calories, protein=product.protein, carbs=product.carbs, fat=product.fat)
    db.add(db_product)
    db.commit()
    return db_product

def get_products_by_name(db: Session, product_name: str, page_number: int):
    products = db.query(models.Product).filter(models.Product.name.contains(product_name)).limit(PRODUCTS_PER_PAGE).offset((page_number) * PRODUCTS_PER_PAGE).all()
    return products

def get_products_by_page_number(db: Session, page_number: int, filter: models.ProductFilter):
    query = db.query(models.Product)
    if filter.id is not None:
        query = query.filter(models.Product.id == filter.id)
    if filter.name is not None:
        query = query.filter(models.Product.name == filter.name)
    if filter.owner is not None:
        query = query.filter(models.Product.owner == filter.owner)
    query = query.limit(PRODUCTS_PER_PAGE).offset((page_number) * PRODUCTS_PER_PAGE)
    return query.all()

def create_order(db: Session, order: schemas.Order):
    db_order = models.Order(product_id=order.product_id, business_id=order.business_id, customer_id=order.customer_id, delivery_address=order.delivery_address, quantity=order.quantity, state=order.state)
    db.add(db_order)
    db.commit()
    return db_order
