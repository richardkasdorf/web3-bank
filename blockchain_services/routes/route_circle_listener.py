from fastapi import Depends, Request, status, APIRouter
from sqlalchemy.orm import Session
from decimal import Decimal
import logging
from db.database import get_db 
from accounts.models import Account, TransactionLedger
from datetime import datetime


logger = logging.getLogger("uvicorn")
router = APIRouter(tags=["Webhook"])

@router.post("/webhooks/circle", status_code=status.HTTP_200_OK)
async def circle_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    notification_type = payload.get("notificationType")
    
    if notification_type == "webhooks.test":
        return {"status": "success"}
    if notification_type not in ["transactions.inbound", "transactions.outbound"]:
        return {"status": "ignored", "reason": "❌ Notification type unmanaged"}
        
    notification = payload.get("notification", {})
    state = notification.get("state")
    circle_wallet_id = notification.get("walletId")
    tx_hash = notification.get("txHash")
    
    if state != "COMPLETE":
        return {"status": "ignored", "reason": f"🔄️ Awaiting settlement. Status: {state}"}
        
    amounts_list = notification.get("amounts", [])
    if not amounts_list:
        return {"status": "error", "message": "🔄️ No value found"}
    amount_value = Decimal(str(amounts_list[0]))
    
    account = db.query(Account).filter(Account.circle_wallet_id == circle_wallet_id).first()
    if not account:
        logger.warning(f"⚠️ Wallet {circle_wallet_id} not found.")
        return {"status": "error", "message": "❌ Account does not exsist"}

    try:
        if notification_type == "transactions.inbound":
            account.balance += amount_value
            
            nova_transacao = TransactionLedger(
                amount=amount_value,
                type="DEPOSIT",
                tx_hash=tx_hash,
                to_account_id=account.user_id,
                from_account_id=None,
                external_from_address=notification.get("sourceAddress"),
                external_to_address=account.wallet_address,
                created_at=datetime.utcnow()
            )
            db.add(nova_transacao)
            logger.info(f"✅ RECEIVED: +{amount_value} USDC to User {account.user_id}")

        elif notification_type == "transactions.outbound":
            account.balance -= amount_value  # ALTERAR DEPOIS PARA DEBITAR AO CLICAR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            nova_transacao = TransactionLedger(
                amount=amount_value,
                type="WITHDRAW",
                tx_hash=tx_hash,
                to_account_id=None,
                from_account_id=account.user_id,
                external_from_address=account.wallet_address,
                external_to_address=notification.get("destinationAddress"),
                created_at=datetime.utcnow()
            )
            db.add(nova_transacao)
            logger.info(f"✅ SENT: -{amount_value} USDC to User {account.user_id}")

        db.commit()
        return {"status": "success", "action": "database_updated"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error updating tables: {str(e)}")
        return {"status": "error", "message": "Internal Error"}
    

