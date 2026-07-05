from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from accounts.models import Account, User
from accounts.schemas import ContaRead
from accounts.auth_model import get_current_user 

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.get("/balance", response_model=ContaRead)
def get_balance(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    
    account = db.query(Account).filter(Account.user_id == current_user.id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This ID account {current_user.id} does not exists."
        )
        
    return account

