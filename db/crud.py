import random
from sqlalchemy.orm import Session
from accounts.models import Account, User
from accounts.auth_model import get_password_hash
from accounts.schemas import CreateAccount, UpdatePassword, CircleWalletData
from fastapi import HTTPException, status
from blockchain_services.circle_wallet.create_wallet import new_wallet


def get_all_accounts(db: Session):
    db.expire_all() 
    return db.query(User).all()

def generate_unique_id(db: Session):
    while True:
        new_id = random.randint(100000, 999999)
        exists = db.query(User).filter(User.id == new_id).first()
        if not exists:
            return new_id

def create_user_with_account(db: Session, user: CreateAccount, wallet: CircleWalletData):
    unique_id = generate_unique_id(db)
    hashed_password = get_password_hash(user.password)

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "E-mail already exists."
        )

    db_user = User(id = unique_id, full_name = user.full_name, email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.flush()

    circle_data = new_wallet()

    new_account = Account(
        user_id = db_user.id, 
        balance = 0.0, 
        wallet_address = circle_data["wallet_address"],
        circle_wallet_id = circle_data["circle_wallet_id"],
        circle_wallet_set_id = circle_data["circle_wallet_set_id"],
        blockchain = circle_data["blockchain"],
        account_type = circle_data["account_type"],
        custody_type = circle_data["custody_type"],
        circle_create_date = circle_data["circle_create_date"]
    )
    db.add(new_account)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



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

## ----------------------------------------- ##

## Blockchain Use

def get_account_by_id(db: Session, user_id: str):
    db_account = db.query(Account).filter(Account.user_id == user_id).first()
    return db_account

## ----------------------------------------- ##






