from db.database import Base
from sqlalchemy import Column, String, Float, Integer, Numeric
from typing import Optional

class Account(Base):
    __tablename__ = "contas"
    
    id_conta = Column(Integer, primary_key=True, index=True)
    titular = Column(String)
    saldo = Column(Numeric(10, 2), nullable=False, default=0.0, server_default="0.0")
    hashed_password = Column(String)
    email = Column(String)
    wallet_address: Optional[str] = Column(String, nullable=True)



