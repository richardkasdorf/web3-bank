from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud
from accounts.schemas import UpdateAccount, ContaRead

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.patch("/update_accounts/{user_id}", response_model=ContaRead)
def patch_account(user_id: str, account_data: UpdateAccount, db: Session = Depends(get_db)):
    update_data = account_data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    db_account = crud.update_account(db, user_id=user_id, update=update_data)
    
    if db_account is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    return db_account



