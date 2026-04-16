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


class UpdatePassword(BaseModel):
    password: str

class InternalTransferRequest(BaseModel):
    id_destino: str
    amount: Decimal






