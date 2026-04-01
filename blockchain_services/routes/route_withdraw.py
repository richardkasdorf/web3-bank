from fastapi import APIRouter, HTTPException, Depends
from decimal import Decimal
from sqlalchemy.orm import Session
from blockchain_services.services.blockchain import transfer_usdc 
from db.crud import get_account_by_id            
from db.database import get_db                                 

router = APIRouter(
    prefix="/blockchain", 
    tags=["Withdraw Stablecoin"]
)

@router.post("/accounts_withdraw/{id_conta}/")
async def withdraw(
    id_conta: str,                                   
    amount: float,
    destination: str = None,                         
    db: Session = Depends(get_db)                    
):
    
    account = get_account_by_id(db, id_conta)
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    amount_decimal = Decimal(str(amount))
    if account.balance < amount_decimal:
        raise HTTPException(status_code=400, detail="Insuficient funds.")

    if not account.wallet_address and not destination:
        raise HTTPException(
            status_code=400, 
            detail="No wallet registred. Inform parameter 'destination'."
        )

    final_destination = destination or account.wallet_address

    try:
        tx_hash = transfer_usdc(final_destination, Decimal(str(amount)))

        return {
            "status": "success",
            "message": "Withdraw successfull",
            "id_conta": id_conta,
            "amount": amount,
            "destination": final_destination,
            "tx_hash": tx_hash,
            "explorer_url": f"https://sepolia.etherscan.io/tx/{tx_hash}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Withdraw error: {str(e)}")
    

