import random
from sqlalchemy.orm import Session
from accounts.models import Account, User
from accounts.auth_model import get_password_hash
from accounts.schemas import CreateAccount, UpdateAccount, UpdatePassword
from fastapi import HTTPException
import os



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

def update_password(db: Session, id_conta: str, password_data: UpdatePassword):
    db_account = db.query(Account).filter(Account.id_conta == id_conta).first()
    if not db_account:
        raise HTTPException(status_code = 404, detail = "Não encontrado")

    db_account.hashed_password = get_password_hash(password_data.password)
    db.commit()
    db.refresh(db_account)
    return db_account


def internal_transfer(db: Session, id_origem: str, id_destino: str, amount: float):
    conta_origem = db.query(Account).filter(Account.id_conta == id_origem).first()
    conta_destino = db.query(Account).filter(Account.id_conta == id_destino).first()

    if not conta_origem:
        return None, f"Account {id_origem} not found."
    if not conta_destino:
        return None, f"Account {id_destino} not found."

    if conta_origem.saldo < amount:
        return None, "Insuficient funds."

    try:
        conta_origem.saldo -= amount
        conta_destino.saldo += amount
        
        db.commit() 
        db.refresh(conta_origem)
        return conta_origem, None
    except Exception as e:
        db.rollback() 
        return None, str(e)

## ----------------------------------------- ##

## Blockchain Use

def get_account_by_id(db: Session, id_conta: str):
    db_account = db.query(Account).filter(Account.id_conta == id_conta).first()
    return db_account

## ----------------------------------------- ##






