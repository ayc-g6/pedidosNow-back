from typing import Union
from pydantic import BaseModel 

# Auth Creation
class AuthBase(BaseModel):
    email: str

class AuthCreationRequestBase(AuthBase):
    password: str

class AuthCustomerCreationRequest(AuthCreationRequestBase):
    username: str

class AuthBusinessCreationRequest(AuthCreationRequestBase):
    business_name: str
    address: str

class AuthCustomerCreationResponse(AuthBase):
    id: str
    username: str
    
class AuthBusinessCreationResponse(AuthBase):
    id: str
    business_name: str
    address: str

class AuthLeak(AuthBase):
    id: str

class User(BaseModel):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Union[str, None] = None