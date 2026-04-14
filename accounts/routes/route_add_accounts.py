from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud   
from accounts.schemas import CreateAccount

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.post("/add_accounts", status_code=201)
async def create_user_with_account(data: CreateAccount, db: Session = Depends(get_db)):
    return crud.create_user_with_account(db, data)


