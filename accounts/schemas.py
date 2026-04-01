from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ContaRead(BaseModel):
    titular: str
    id_conta: int
    saldo: float
    hashed_password: str
    email: Optional[str] = None
    class Config:
        from_attributes = True

class AccountCreate(BaseModel):
    titular: str
    email: str
    hashed_password: str

class UpateAccount(BaseModel):
    titular: Optional[str] = None
    saldo: Optional[float] = None
    
class UpdatePassword(BaseModel):
    password: str

class InternalTransferRequest(BaseModel):
    id_destino: str
    amount: Decimal






