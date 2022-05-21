from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/auth/", response_model=schemas.Auth)
def create_auth(auth: schemas.AuthCreate, db: Session = Depends(get_db)):
    db_auth = crud.get_auth_by_email(db, email=auth.email)
    if db_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_auth(db, auth)

@app.get('/auth/', response_model=List[schemas.Auth])
def read_auths(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_auths(db, skip=skip, limit=limit)
