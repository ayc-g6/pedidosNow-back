from sqlalchemy.orm import Session

from . import models, schemas

def get_auth_by_email(db: Session, email: str):
    return db.query(models.Auth).filter(models.Auth.email == email).first()

def create_auth(db: Session, auth: schemas.AuthCreate):
    hashed_password = auth.password # TODO Hash password
    db_auth = models.Auth(email=auth.email, hashed_password=hashed_password)
    db.add(db_auth)
    db.commit()
    db.refresh()
    return db_auth