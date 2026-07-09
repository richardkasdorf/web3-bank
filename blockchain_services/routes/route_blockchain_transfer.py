from fastapi import Depends, status, APIRouter, HTTPException
from accounts.auth_model import get_current_user 
from accounts.schemas import TransferRequest
from accounts.models import Account, User
from sqlalchemy.orm import Session
from db.database import get_db
from circle.web3 import utils, developer_controlled_wallets
from decimal import Decimal
from blockchain_services.blockchain_transfer import resolve_destination
import os
from blockchain_services.services.decrypt import decrypt_data

router = APIRouter(prefix="/transactions", tags=["transfer"])


@router.post("/transfer", status_code=status.HTTP_201_CREATED)
async def initiate_transfer(payload: TransferRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    source_account = db.query(Account).filter(Account.user_id == current_user.id).first()

    if not source_account:
        raise HTTPException(status_code=404, detail="❌ Account not found.")
        
    if source_account.balance < Decimal(str(payload.amount)):
        raise HTTPException(status_code=400, detail="❌ Insuficient balance.")
    
    resolved_destination_address = resolve_destination(payload.destination, db)

    hex_encoded = decrypt_data()

    client = utils.init_developer_controlled_wallets_client(
        api_key=os.getenv("CIRCLE_API_KEY"),
        entity_secret=hex_encoded
    )

    transactions_api = developer_controlled_wallets.TransactionsApi(client)

    try:
        request_payload = developer_controlled_wallets.CreateTransferTransactionForDeveloperRequest.from_dict({
            "walletAddress": source_account.wallet_address,
            "blockchain": source_account.blockchain,
            "destinationAddress": resolved_destination_address,
            "tokenAddress": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238", # Contrato USDC Sepolia
            "amounts": [f"{payload.amount:.6f}"],
            "feeLevel": "MEDIUM"
        })
        
        transfer_response = transactions_api.create_developer_transaction_transfer(request_payload)
        transfer_data = transfer_response.data.to_dict()
        
        return {
            "status": "initiated",
            "message": "✅ Transfer sent to Circle.",
            "circle_transaction_id": transfer_data.get("id"),
            "resolved_destination": resolved_destination_address,
            "state": transfer_data.get("state")
        }

    except developer_controlled_wallets.ApiException as e:
        print("Exception when calling the Circle Transactions API: %s\n" % e)
        raise HTTPException(status_code=502, detail=f"❌ Circle API Error: {str(e)}")




