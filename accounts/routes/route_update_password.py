from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud
from accounts.schemas import UpdatePassword, ContaRead
from accounts.auth_model import get_current_user
from accounts.models import Account

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.patch("/update_password")
def patch_account(password_data: UpdatePassword, db: Session = Depends(get_db), current_user: Account = Depends(get_current_user)):
    
    db_account = crud.update_password(db, user_id = current_user.user_id, password_data = password_data)
    if db_account is None:
        raise HTTPException(status_code=404, detail = "Account not found")
    return {"message": "Password update is complete!"}



