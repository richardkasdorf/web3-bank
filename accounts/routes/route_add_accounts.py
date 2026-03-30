from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud   
from accounts.schemas import AccountCreate

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.post("/add_accounts", status_code=201)
async def add_account(data: AccountCreate, db: Session = Depends(get_db)):
    return crud.add_account(db, data)


