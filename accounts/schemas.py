from pydantic import BaseModel, EmailStr
from typing import Optional
from decimal import Decimal


class CreateAccount(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class ContaRead(BaseModel):
    titular: str
    id: int
    saldo: float
    hashed_password: str
    email: Optional[str] = None
    class Config:
        from_attributes = True

class UpateAccount(BaseModel):
    titular: Optional[str] = None
    saldo: Optional[float] = None
    
class UpdatePassword(BaseModel):
    password: str

class InternalTransferRequest(BaseModel):
    id_destino: str
    amount: Decimal






