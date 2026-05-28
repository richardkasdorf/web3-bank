from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db  
from db import crud   
from accounts.schemas import CreateAccount, CircleWalletData 

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.post("/add_accounts", status_code=201)

async def create_user_with_account(data: CreateAccount, db: Session = Depends(get_db)):
    
    try:
        return crud.create_user_with_account(db=db, user=data, wallet=None)
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na rota: {str(e)}")


