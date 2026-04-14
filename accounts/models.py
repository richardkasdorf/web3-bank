from db.database import Base
from sqlalchemy import Column, String, Float, Integer, Numeric, ForeignKey, DateTime
from typing import Optional
from sqlalchemy.orm import relationship
from datetime import datetime

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Numeric(precision=20, scale=6), default=0.0)
    wallet_address = Column(String, unique=True)
    owner = relationship("User", back_populates="account")
    transactions_from = relationship("TransactionLedger", foreign_keys="[TransactionLedger.from_account_id]")
    transactions_to = relationship("TransactionLedger", foreign_keys="[TransactionLedger.to_account_id]")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    account = relationship("Account", back_populates="owner", uselist=False)

class TransactionLedger(Base):
    __tablename__ = "transactions_ledger"

    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    amount = Column(Numeric(precision=20, scale=6))
    type = Column(String)
    tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


