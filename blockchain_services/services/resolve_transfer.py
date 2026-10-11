from sqlalchemy.orm import Session
from accounts.models import Account
from fastapi import HTTPException


#Singleton ou um Cache LRU para a MASTER_KEY

def resolve_destination(destination: str, db: Session) -> str:

    destination = destination.strip()
    
    if destination.startswith("0x"):
        if len(destination) != 42:
            raise HTTPException(status_code=400, detail="❌ Invalid wallet address.")
        return destination
        
    if destination.isdigit() and len(destination) == 6:
        account_destination = db.query(Account).filter(Account.user_id == int(destination)).first()
        if not account_destination:
            raise HTTPException(
                status_code=404, 
                detail= f"❌ Account '{destination}' not found."
            )
        return account_destination.wallet_address
        
    raise HTTPException(
        status_code=400, 
        detail="❌ Invalid destination. Enter a 6-digit account number or an address starting with 0x."
    )

