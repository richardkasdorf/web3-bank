from pydantic import BaseModel, EmailStr
from typing import Optional
from decimal import Decimal


class CreateAccount(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UpdateAccount(BaseModel):
    email: EmailStr

class ContaRead(BaseModel):
    full_name: str
    email: EmailStr
    class Config:
        from_attributes = True

class UpdatePassword(BaseModel):
    password: str

class InternalTransferRequest(BaseModel):
    from_account_id: int  
    to_account_id: int    
    amount: Decimal






