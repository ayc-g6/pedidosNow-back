from curses.ascii import HT
from datetime import datetime, timedelta
from typing import List, Union
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Required
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from auth import authenticate_scope, authenticate_user, create_access_token, get_current_id, get_password_hash

import crud, models, schemas
from database import get_db, engine

ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
	allow_headers=["*"],
    max_age=3600,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.delete("/delete")
def delete_database(db: Session = Depends(get_db)):
    crud.delete_database(db)
    return True

""" Sign Up Customer."""
@app.post("/customer/", response_model=schemas.AuthCustomerCreationResponse)
def create_customer(auth_customer: schemas.AuthCustomerCreationRequest, db: Session = Depends(get_db)):
    db_auth = crud.get_auth_by_email(db, email=auth_customer.email)
    if db_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    auth_customer.password = get_password_hash(auth_customer.password)
    return crud.create_customer(db, auth_customer)

""" Sign Up Delivery."""
@app.post("/delivery/", response_model=schemas.AuthDeliveryCreationResponse)
def create_delivery(auth_delivery: schemas.AuthDeliveryCreationRequest, db: Session = Depends(get_db)):
    db_auth = crud.get_auth_by_email(db, email=auth_delivery.email)
    if db_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    auth_delivery.password = get_password_hash(auth_delivery.password)
    return crud.create_delivery(db, auth_delivery)

""" Get Business Profile"""
@app.get("/business")
def read_business_self(current_user: schemas.TokenData = Depends(get_current_id), db: Session = Depends(get_db)):
    return crud.get_business(db, current_user.id)

@app.get("/business/{business_id}")
def read_business(business_id: str, db: Session = Depends(get_db)):
    db_business = crud.get_business(db, business_id)
    if not db_business:
        raise HTTPException(status_code=404, detail="Business not found")
    return db_business

""" Sign Up Business."""
@app.post("/business/", response_model=schemas.AuthBusinessCreationResponse)
def create_business(auth_business: schemas.AuthBusinessCreationRequest, db: Session = Depends(get_db)):
    db_auth = crud.get_auth_by_email(db, email=auth_business.email)
    if db_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    auth_business.password = get_password_hash(auth_business.password)
    return crud.create_business(db, auth_business)  

""" Login General."""
@app.post("/token/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_id = authenticate_user(form_data.username, form_data.password, db)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    scope = authenticate_scope(user_id, form_data.scopes, db)
    return {'access_token': access_token, "token_type": "bearer", "scope": scope}

""" Productos."""
@app.post("/product/")
def create_product(product: schemas.ProductBase, current_user: schemas.TokenData = Depends(get_current_id), db: Session = Depends(get_db)):
    return crud.create_product(db, product, current_user.id)

@app.get("/product/all/{page_number}")
def get_product(page_number: int, db: Session = Depends(get_db), id: Union[int, None] = None, name: Union[str, None] = None, owner_id: Union[str, None] = None):
    products = crud.get_products_by_page_number(db, page_number, id, name, owner_id)
    return products

@app.get("/business/product/{page_number}")
def get_business_product(page_number: int, id: Union[int, None] = None, name: Union[str, None] = None, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(get_current_id)):
    current_user.id
    products = crud.get_products_by_page_number(db, page_number, id, name, current_user.id)
    return products

""" Ordenes."""
@app.get("/order/all/{page_number}")
def get_orders(page_number: int, states : Union[List[int], None] = Query(default=None), db: Session = Depends(get_db)):
    orders = crud.get_orders_by_page_number(db, page_number, None, None, states)
    return orders

@app.post("/order/")
def create_order(order: schemas.OrderBase, current_user: schemas.TokenData = Depends(get_current_id), db: Session = Depends(get_db)):
    customer_id = current_user.id
    return crud.create_order(db, order, customer_id)

@app.get("/business/order/{page_number}")
def get_business_orders(page_number: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(get_current_id)):
    orders = crud.get_orders_by_page_number(db, page_number, None, current_user.id, [1,2])
    return orders

@app.get("/customer/order/{page_number}")
def get_customer_orders(page_number: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(get_current_id)):
    orders = crud.get_orders_by_page_number(db, page_number, current_user.id, None, None)
    return orders

@app.get("/order/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.patch("/order/{order_id}")
def update_order(order_id: int, state: int = Query(ge=1, le=4), current_user: schemas.TokenData = Depends(get_current_id), db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if state < order.state:
        raise HTTPException(status_code=409, detail="Order state is higher than state received")
    if order.state == 0 and not crud.is_delivery(db, current_user.id):
        raise HTTPException(status_code=403, detail="User is not delivery")
    if order.state == 1 and current_user.id != order.business_id:
        raise HTTPException(status_code=403, detail="User is not owner of order products")
    if order.state >= 2 and current_user.id != crud.get_order_delivery_by_id(db, order_id).delivery_id:
        raise HTTPException(status_code=403, detail="User is not delivery of order")
    updated_order = crud.update_order(db, order, state, current_user.id)
    if order.state == 4:
        crud.delete_order_delivery_by_id(db, order_id)
    return updated_order

@app.get("/delivery/order")
def get_current_work(current_user: schemas.TokenData = Depends(get_current_id), db: Session = Depends(get_db)):
    work = crud.get_order_delivery_by_delivery(db, current_user.id)
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    return work
