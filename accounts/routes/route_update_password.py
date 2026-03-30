from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud
from accounts.schemas import UpdatePassword, ContaRead

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.patch("/update_password/{id_conta}", response_model = ContaRead)
def patch_account(id_conta: str, password_data: UpdatePassword, db: Session = Depends(get_db)):
    
    db_account = crud.update_password(db, id_conta = id_conta, password_data = password_data)
    if db_account is None:
        raise HTTPException(status_code=404, detail = "Conta não encontrada")
    return db_account



