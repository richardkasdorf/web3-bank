from pydantic import BaseModel, EmailStr, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from typing import List, Optional


class CreateAccount(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UpdatePassword(BaseModel):
    password: str

class UpdateAccount(BaseModel):
    email: EmailStr

class CircleWalletData(BaseModel):
    wallet_id: UUID = Field(..., alias="id", description="Circle unic ID")
    wallet_set_id: UUID = Field(..., description="wallet_set ID")
    address: str = Field(..., description="Public address")
    blockchain: str = Field(..., description="Blockchain (ex: ETH-SEPOLIA)")
    account_type: str = Field(..., description="Account type (ex: EOA / SCA)")
    custody_type: str = Field(..., description="Custody type")
    create_date: datetime = Field(..., description="Created at")

    class Config:
        populate_by_name = True 


class ContaRead(BaseModel):
    id: int = Field(..., description="ID interno da conta no banco de dados")
    user_id: int = Field(..., description="ID do usuário proprietário desta conta")
    balance: Decimal = Field(..., description="Saldo atual da conta")
    wallet_address: str = Field(..., description="Endereço público da carteira (Chave Pública)")
    blockchain: str = Field(..., description="Rede blockchain configurada (ex: ETH-SEPOLIA)")
    account_type: str = Field(..., description="Tipo de conta na blockchain (ex: EOA)")
    custody_type: str = Field(..., description="Tipo de custódia da carteira (ex: DEVELOPER)")
    circle_wallet_id: Optional[str] = Field(None, description="ID único da carteira dentro da plataforma Circle")
    circle_wallet_set_id: Optional[str] = Field(None, description="ID do conjunto de carteiras associado na Circle")
    circle_create_date: Optional[datetime] = Field(None, description="Data e hora exata em que a carteira foi criada na Circle")
    

class TransferRequest(BaseModel):
    from_user_id: int = Field(..., description="ID de quem está enviando (6 dígitos)")
    destination: str = Field(..., description="Digite o número da conta (6 dígitos) OU o endereço da Wallet (0x...)")
    amount: float = Field(..., description="Valor em USDC a ser transferido")





