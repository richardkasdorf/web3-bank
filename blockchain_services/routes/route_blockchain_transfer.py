from fastapi import APIRouter, Depends, HTTPException, status
from blockchain_services.blockchain_transfer import transfer_usdc 
from accounts.auth_model import get_current_user 
from accounts.schemas import ExternalTransferRequest
from accounts.models import User, Account
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()

@router.post("/transfer/external", status_code = status.HTTP_201_CREATED)
async def external_transfer(request: ExternalTransferRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    source_account = db.query(Account).filter(Account.user_id == current_user.id).first()
    if not source_account: raise HTTPException(status_code = 403, detail = "You have no permission or account does not exists.")

    if source_account.balance < request.amount:
        raise HTTPException(status_code = 400, detail = "Insufficient internal balance.")

    try:
        tx_hash = transfer_usdc(
            db,
            external_from_address = source_account.wallet_address,
            external_to_address = request.external_to_address, 
            amount = request.amount
        )

        return {
            "message": "Transfer Successful!",
            "tx_hash": tx_hash,
            "explorer_url": f"https://sepolia.etherscan.io/tx/{tx_hash}"
        }

    except ValueError as ve:
        raise HTTPException(status_code = 400, detail = str(ve))
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Blockchain error: {str(e)}")

