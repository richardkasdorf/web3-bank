from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud
from accounts.schemas import UpateAccount, ContaRead

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.patch("/update_accounts/{id_conta}", response_model = ContaRead)
def patch_account(id_conta: str, account_data: UpateAccount, db: Session = Depends(get_db)):
    
    db_account = crud.update_account(db, id_conta = id_conta, account_data = account_data)
    if db_account is None:
        raise HTTPException(status_code=404, detail = "Conta não encontrada")
    return db_account


