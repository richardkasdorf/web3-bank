import random
from sqlalchemy.orm import Session
from accounts.models import Account, User, TransactionLedger
from accounts.auth_model import get_password_hash
from accounts.schemas import CreateAccount, UpdateAccount, UpdatePassword
from fastapi import HTTPException, status
import os
from decimal import Decimal



def get_all_accounts(db: Session):
    db.expire_all() 
    return db.query(User).all()

def generate_unique_id(db: Session):
    while True:
        new_id = random.randint(100000, 999999)
        exists = db.query(User).filter(User.id == new_id).first()
        if not exists:
            return new_id

def create_user_with_account(db: Session, user: CreateAccount):
    unique_id = generate_unique_id(db)
    hashed_password = get_password_hash(user.password)

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail already exists."
        )

    db_user = User(id=unique_id, full_name=user.full_name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)

    db.flush()

    new_account = Account(user_id=db_user.id, balance=0.0, wallet_address=f"0x{os.urandom(20).hex()}")
    db.add(new_account)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def update_account(db: Session, user_id: int, update: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code = 404, detail = "Not found!")

    for field, value in update.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

## ----------------------------------------- ##

## CLIENTE ONLY

def update_password(db: Session, user_id: int, password_data: UpdatePassword):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code = 404, detail = "Not found!")

    db_user.hashed_password = get_password_hash(password_data.password)
    db.commit()
    db.refresh(db_user)
    return True



def internal_transfer(db: Session, from_user_id: int, to_user_id: int, amount: Decimal):
    from_acc = db.query(Account).filter(Account.user_id == from_user_id).first()
    to_acc = db.query(Account).filter(Account.user_id == to_user_id).first()

    if not from_acc or not to_acc:
        return None, "Account not found."

    if from_acc.balance < amount:
        return None, "Insuficient balance."

    try:
        from_acc.balance -= amount
        to_acc.balance += amount

        new_transaction = TransactionLedger(
            from_account_id = from_acc.user_id,
            to_account_id = to_acc.user_id,
            amount = amount,
            type = "INTERNAL_TRANSFER"
        )
        db.add(new_transaction)

        db.commit()
        db.refresh(from_acc)
        
        return from_acc, "Transaction successful."

    except Exception as e:
        db.rollback()
        return None, f"Error: {str(e)}"


## ----------------------------------------- ##

## Blockchain Use

def get_account_by_id(db: Session, id_conta: str):
    db_account = db.query(Account).filter(Account.id_conta == id_conta).first()
    return db_account

## ----------------------------------------- ##






