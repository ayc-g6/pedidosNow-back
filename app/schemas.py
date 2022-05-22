from pydantic import BaseModel 


class ProductBase(BaseModel):
    name: str
    price: float
    owner: str

class AuthBase(BaseModel):
    email: str

class AuthCustomerCreate(AuthBase):
    username: str
    password: str

class AuthBusinessCreate(AuthBase):
    business_name: str
    address: str
    password: str

class Auth(AuthBase):
    id: str

    class Config:
        orm_mode = True
