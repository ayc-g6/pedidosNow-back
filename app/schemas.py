from pydantic import BaseModel 

class AuthBase(BaseModel):
    email: str

class AuthCreate(AuthBase):
    password: str

class Auth(AuthBase):
    id: str

    class Config:
        orm_mode = True