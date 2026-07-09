from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from accounts.models import Account, TransactionLedger, User
from accounts.schemas import TransactionRead
from accounts.auth_model import get_current_user

router = APIRouter(
    prefix="/accounts",
    tags=["Account Statement"]
)

@router.get("/statement", response_model=List[TransactionRead])
def get_statement(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    account = db.query(Account).filter(Account.user_id == current_user.id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta bancária não encontrada para este usuário."
        )

    transactions = db.query(TransactionLedger).filter(
        (TransactionLedger.from_account_id == current_user.id) | 
        (TransactionLedger.to_account_id == current_user.id)
    ).order_by(TransactionLedger.created_at.desc()).all()

    return transactions
