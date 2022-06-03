from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
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

@app.delete("/delete/products")
def delete_products_database(db: Session = Depends(get_db)):
    crud.delete_database_products(db)
    return True

""" Sign Up Customer."""
@app.post("/customer/", response_model=schemas.AuthCustomerCreationResponse)
def create_customer(auth_customer: schemas.AuthCustomerCreationRequest, db: Session = Depends(get_db)):
    db_auth = crud.get_auth_by_email(db, email=auth_customer.email)
    if db_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    auth_customer.password = get_password_hash(auth_customer.password)
    return crud.create_customer(db, auth_customer)

""" Get Business Profile"""
@app.get("/business/{business_id}", response_model=schemas.BusinessProfileResponse)
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

# FIXME Deprecado y sera borrado
""" Returns your user ID."""
@app.get("/token/", response_model=schemas.TokenData)
def read_token(current_user: schemas.User = Depends(get_current_id)):
    return current_user


""" Login General."""
@app.post("/token/", response_model=schemas.Token)
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
    with open("log.txt", "w+") as my_log:
        my_log.write(f"{form_data.scopes}\n")
        my_log.write(f"{form_data}\n")
    return {'access_token': access_token, "token_type": "bearer", "scope": scope}

""" Productos."""
@app.post("/product/")
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/product/all/{page_number}")
def get_product(page_number: int, db: Session = Depends(get_db)):
    products = crud.get_products_by_page_number(db, page_number)
    return products

@app.get("/product/{product_name}/{page_number}")
def get_products_by_name(product_name: str, page_number: int, db: Session = Depends(get_db)):
    products = crud.get_products_by_name(db, product_name, page_number)
    return products

""" Ordenes."""
@app.post("/order/")
def create_order(order: schemas.Order, db: Session = Depends(get_db)):
    return crud.create_order(db, order.product_id, order.customer_id)