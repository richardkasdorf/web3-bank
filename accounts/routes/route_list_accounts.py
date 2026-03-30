from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud              

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.get("/get_accounts")
def list_accounts(db: Session = Depends(get_db)):
    return crud.get_all_accounts(db)




