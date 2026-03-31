import os, time, random
from sqlalchemy.orm import Session
from accounts.models import Account
from accounts.auth_model import get_password_hash
from accounts.schemas import AccountCreate, UpateAccount, UpdatePassword
from fastapi import HTTPException, Depends
from typing import Annotated



## ADMIN ONLY

def get_all_accounts(db: Session):
    db.expire_all() 
    return db.query(Account).all()

def generate_unique_id(db: Session):
    while True:
        new_id = random.randint(100000, 999999)
        exists = db.query(Account).filter(Account.id_conta == new_id).first()
        if not exists:
            return new_id

def add_account(db: Session, account_data: AccountCreate):
    unique_id = generate_unique_id(db)

    db_account = Account(
        titular = account_data.titular,
        id_conta = unique_id,
        email = account_data.email,
        hashed_password = get_password_hash(account_data.hashed_password))
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, id_conta: str, account_data: UpateAccount):
    db_account = db.query(Account).filter(Account.id_conta == id_conta).first()
    if not db_account:
        raise HTTPException(status_code = 404, detail = "Não encontrado")

    update_data = account_data.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

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






