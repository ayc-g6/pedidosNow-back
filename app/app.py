from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import authenticate_user, create_access_token, get_current_id, get_password_hash

import crud, models, schemas
from database import get_db, engine

ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World "}


""" Sign Up Customer."""
@app.post("/customer/", response_model=schemas.AuthCustomerCreationResponse)
def create_customer(auth_customer: schemas.AuthCustomerCreationRequest, db: Session = Depends(get_db)):
    db_auth = crud.get_auth_by_email(db, email=auth_customer.email)
    if db_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    auth_customer.password = get_password_hash(auth_customer.password)
    return crud.create_customer(db, auth_customer)


""" Sign Up Business."""
@app.post("/business/", response_model=schemas.AuthBusinessCreationResponse)
def create_business(auth_business: schemas.AuthBusinessCreationRequest, db: Session = Depends(get_db)):
    db_auth = crud.get_auth_by_email(db, email=auth_business.email)
    if db_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_business(db, auth_business)  


@app.get('/auth/')
def leak_auths(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_auths(db, skip=skip, limit=limit)


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
    return {'access_token': access_token, "token_type": "bearer"}


@app.post("/product/")
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    return crud.create_product(db, product)
