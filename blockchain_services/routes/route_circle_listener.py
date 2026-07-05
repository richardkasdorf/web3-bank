from fastapi import Depends, Request, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from decimal import Decimal
import logging
import time
from db.database import get_db 
from accounts.models import Account, TransactionLedger
from datetime import datetime

logger = logging.getLogger("uvicorn")
router = APIRouter(tags=["Webhook"])

@router.post("/webhooks/circle", status_code=status.HTTP_200_OK)
async def circle_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    notification_type = payload.get("notificationType")

    logger.info(f"📩 WEBHOOK RECEIVED - Tipo: {notification_type}")
    
    if notification_type == "webhooks.test":
        return {"status": "success"}
    if notification_type not in ["transactions.inbound", "transactions.outbound"]:
        return {"status": "ignored", "reason": "❌ Notification type unmanaged"}
        
    notification = payload.get("notification", {})
    state = notification.get("state")
    circle_wallet_id = notification.get("walletId")
    tx_hash = notification.get("txHash")
    
    logger.info(f"🔍 Tx Status: {tx_hash} | Circle State: {state}")
    
    if state not in ["CONFIRMED", "COMPLETE"]:
        return {"status": "ignored", "reason": f"🔄️ Awaiting settlement. Status: {state}"}
        
    amounts_list = notification.get("amounts", [])
    if not amounts_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="🔄️ No value found")
    
    try:
        raw_amount = str(amounts_list[0]) if isinstance(amounts_list, list) else str(amounts_list)
        if "." not in raw_amount:
            amount_value = Decimal(raw_amount) / Decimal("1000000")
        else:
            amount_value = Decimal(raw_amount)
    except Exception as parse_err:
        logger.error(f"❌ Error parsing amount {amounts_list}: {str(parse_err)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount format")
    
    max_retries = 3
    retry_delay = 3

    for attempt in range(max_retries):
        try:

            current_action_type = "DEPOSIT" if notification_type == "transactions.inbound" else "WITHDRAW"

            already_processed = db.query(TransactionLedger).filter(TransactionLedger.tx_hash == tx_hash, TransactionLedger.type == current_action_type).first()

            if already_processed:
                logger.info(f"⚠️ Transaction {tx_hash} already processed down. Skipping.")
                return {"status": "success", "action": "already_processed"}

            account = db.query(Account).filter(Account.circle_wallet_id == circle_wallet_id).first()
            if not account:
                logger.warning(f"⚠️ Wallet {circle_wallet_id} not found.")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="❌ Account does not exist")

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
                logger.info(f"✅ RECEIVED & COMMITTED: +{amount_value} USDC to User {account.user_id}")

            elif notification_type == "transactions.outbound":
                account.balance -= amount_value
                
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
                logger.info(f"🔻 SENT & COMMITTED: -{amount_value} USDC to User {account.user_id}")

            db.commit()
            return {"status": "success", "action": "database_updated"}
            
        except OperationalError as op_err:
            db.rollback()
            if attempt == max_retries - 1:
                logger.critical(f"❌ Neon database connection failed: {str(op_err)}")
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection failed")
            
            logger.warning(f"⚠️ Neon in Cold Start. Attempt {attempt + 1} failed. Waiting {retry_delay}s...")
            time.sleep(retry_delay)

        except HTTPException as http_ex:
            db.rollback()
            raise http_ex

        except Exception as e:
            db.rollback()
            logger.error(f"❌ Database error: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
