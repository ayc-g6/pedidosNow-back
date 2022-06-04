from typing import Union
from pydantic import BaseModel 

# Auth Creation
class AuthBase(BaseModel):
    email: str

class AuthCreationRequestBase(AuthBase):
    password: str

class AuthDeliveryCreationRequest(AuthCreationRequestBase):
    username: str

class AuthCustomerCreationRequest(AuthCreationRequestBase):
    username: str

class AuthBusinessCreationRequest(AuthCreationRequestBase):
    business_name: str
    address: str

class AuthCustomerCreationResponse(AuthBase):
    id: str
    username: str

class AuthDeliveryCreationResponse(AuthBase):
    id: str
    username: str

class AuthBusinessCreationResponse(AuthBase):
    id: str
    business_name: str
    address: str

# Login Related
class Token(BaseModel):
    access_token: str
    token_type: str
    scope: str

class TokenData(BaseModel):
    id: Union[str, None] = None

# Business Related
class BusinessProfileResponse(BaseModel):
    id: str
    business_name: str
    address: str
    
# Product Related
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    calories: float
    protein: float
    carbs: float
    fat: float

# Order Related
class OrderBase(BaseModel):
    product_id: str
    business_id: str
    delivery_address: str
    quantity: int
   

class Order(OrderBase):
    id: int
    customer_id: str
    state: int
    
