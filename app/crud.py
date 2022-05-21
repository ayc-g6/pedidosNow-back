from sqlalchemy.orm import Session
import uuid

import models, schemas

def get_auth_by_email(db: Session, email: str):
    return db.query(models.Auth).filter(models.Auth.email == email).first()

def get_auths(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Auth).offset(skip).limit(limit).all()

def create_auth(db: Session, auth: schemas.AuthCreate):
    hashed_password = auth.password # TODO Hash password
    db_auth = models.Auth(email=auth.email, hashed_password=hashed_password)
    db.add(db_auth)
    db.commit()
    db.refresh(db_auth)
    return db_auth
