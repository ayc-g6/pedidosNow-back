from datetime import datetime, timedelta
from typing import List, Union
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

import schemas, crud

SECRET_KEY = "367d57f766d20336be01f360637ccddfad8e6354d7878d4d2c499d0f9aac12ab"
ALGORITHM = "HS256"

VALID_SCOPES = {'business', 'customer', 'delivery'}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token/')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str, db: Session):
    db_auth = crud.get_auth_by_email(db, email=email)
    if not db_auth:
        return False
    if not verify_password(password, db_auth.hashed_password):
        return False
    return db_auth.id

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

""" Receives the id of a valid user and a list of scopes.
    Throws an HTTPException if:
    - Any of the scopes is not valid
    - The real scope of the user is not in the scopes
    Returns the real scope.
"""
def authenticate_scope(id: str, scopes: List[str], db: Session):
    scope_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid scope",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(scopes)
    for scope in scopes:
        if scope not in VALID_SCOPES:
            raise scope_exception
    scope = get_scope(id, db)
    if scope not in scopes:
        raise scope_exception
    return scope

""" Receives the id of a valid user and returns the scope (or account type).
    If the id is not from a valid user, None is returned.
"""
def get_scope(id: str, db: Session):
    print(id)
    if crud.is_business(db, id):
        print('bus')
        return 'business'
    if crud.is_customer(db, id):
        print('cus')
        return 'customer'
    if crud.is_delivery(db, id):
        print('del')
        return 'delivery'
    print('non')
    return None

""" Receives an access token and returns the user id."""
def get_current_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception     
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data