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

class TransactionRead(BaseModel):
    id: int
    amount: Decimal
    type: str
    tx_hash: Optional[str] = None
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    external_from_address: Optional[str] = None
    external_to_address: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

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
    id: int = Field(..., description="Internal account ID in the database")
    user_id: int = Field(..., description="ID of the user who owns this account")
    balance: Decimal = Field(..., description="Current account balance in USDC")
    eth_balance: Decimal = Field(..., description="Current account balance in ETH")
    wallet_address: str = Field(..., description="Public wallet address (Public Key)")
    blockchain: str = Field(..., description="Configured blockchain network (e.g., ETH-SEPOLIA)")
    account_type: str = Field(..., description="Blockchain account type (e.g., EOA)")
    custody_type: str = Field(..., description="Wallet custody type (e.g., DEVELOPER)")
    circle_wallet_id: Optional[str] = Field(None, description="Unique wallet ID within the Circle platform")
    circle_wallet_set_id: Optional[str] = Field(None, description="ID of the associated wallet set in Circle")
    circle_create_date: Optional[datetime] = Field(None, description="Exact date and time when the wallet was created in Circle")
    

class TransferRequest(BaseModel):
    destination: str = Field(..., description="Enter the account number (6 digits) OR the Wallet address (0x...)")
    amount: float = Field(..., description="Amount in USDC to be transferred")





