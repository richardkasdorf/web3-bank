from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from accounts.schemas import InternalTransferRequest
from accounts.auth_model import get_current_user
from accounts.models import Account, User

router = APIRouter(prefix = "/accounts", tags = ["Intrabank Transfer"])

@router.post("/transfer")
def transfer_between_accounts(data: InternalTransferRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    source_account = db.query(Account).filter(Account.user_id == current_user.id).first()

    if not source_account: raise HTTPException(status_code = 403, detail = "You have no permission or account does not exists.")

    account, erro = crud.internal_transfer(
        db, 
        from_user_id = source_account.user_id, 
        to_user_id = data.to_account_id, 
        amount = data.amount
    )

    if erro:
        raise HTTPException(status_code = 400, detail = erro)

    return {
        "message": "Transaction completed!",
        "new_balance": float(account.balance) 
    }

