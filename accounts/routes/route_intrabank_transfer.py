from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from accounts.schemas import InternalTransferRequest
from accounts.auth_model import get_current_user
from accounts.models import Account

router = APIRouter(prefix="/accounts", tags=["Intrabank Transfer"])

@router.post("/transfer")
def transfer_between_accounts(data: InternalTransferRequest, current_user: Account = Depends(get_current_user), db: Session = Depends(get_db)):
    
    conta, erro = crud.internal_transfer(
        db, current_user.id_conta, data.id_destino, data.amount
    )

    if erro:
        status = 404 if "existem" in erro else 400
        raise HTTPException(status_code=status, detail=erro)

    return {
        "message": "Transferência realizada!",
        "novo_saldo": conta.saldo
    }
