from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from accounts.schemas import InternalTransferRequest

router = APIRouter(prefix="/accounts", tags=["Intrabank Transfer"])

@router.post("/transfer")
def transfer_between_accounts(
    data: InternalTransferRequest, 
    db: Session = Depends(get_db)
):
    
    conta, erro = crud.internal_transfer(
        db, data.id_origem, data.id_destino, data.amount
    )

    if erro:
        status = 404 if "existem" in erro else 400
        raise HTTPException(status_code=status, detail=erro)

    return {
        "message": "Transferência realizada!",
        "novo_saldo": conta.saldo
    }
