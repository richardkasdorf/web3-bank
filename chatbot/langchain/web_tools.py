import os
from langchain.tools import tool
from dotenv import load_dotenv
from typing import Optional
from chatbot.models import TransactionsArgs, ClientArgs
from db.database import get_db_session
from accounts.models import TransactionLedger, User, Account
from sqlalchemy import or_
import contextvars


load_dotenv()

current_user_id: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar(
    "current_user_id", default=None
)

@tool("get_transactions", args_schema=TransactionsArgs)
def get_user_transactions(limit: int = 5):
    """Consults the transaction statement of the authenticated user in the database.
    Use this tool whenever the user asks to see their statement, balance,
    transaction history, or amounts sent or received in USDC.
    It is not necessary to provide an account or user ID — the query is always
    made for the user already authenticated in the current session."""
    user_id = current_user_id.get()
    if not user_id:
        return "Error: It was not possible to identify the authenticated user to view the statement."
    db = get_db_session()

    try:
        transactions = (
            db.query(TransactionLedger)
            .filter(
                or_(
                    TransactionLedger.from_account_id == user_id,
                    TransactionLedger.to_account_id == user_id
                )
            )
            .order_by(TransactionLedger.id.desc())
            .limit(limit)
            .all()
        )
        if not transactions:
            return "No transactions found for this user."
        
        tx_list = []
        for tx in transactions:
            direction = "received" if tx.to_account_id == user_id else "sent"
            tx_list.append({
                "hash": tx.tx_hash,
                "type": tx.type,
                "direction": direction,
                "amount": float(tx.amount) if tx.amount is not None else "N/A",
                "data": tx.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(tx, 'created_at') else "N/A"
            })
        return tx_list
    except Exception as e:
        print(f"[Database Neon Error]: {e}")
        return []
    finally:
        db.close()



@tool("get_profile", args_schema=ClientArgs)
def get_user_profile() -> str:
    """RULE: Return ONLY what the user asks for. If asked about their investor profile, 
    respond only with their profile, e.g., Moderate, aggressive, defensive.
    This function is used to return certain personal data that does not compromise security, 
    such as balance, registered email, operating blockchain, investor profile..."""
    user_id = current_user_id.get()
    if not user_id:
        return "Error: It was not possible to identify the authenticated user to view the statement."
    db = get_db_session()

    try:
        user = db.query(User).filter(User.id == user_id).first()
        account = db.query(Account).filter(Account.user_id == user_id).first()

        profile = (
            {
                "name": user.full_name,
                "email": user.email,
                "investor_profile": user.investor_profile,
            }
            if user
            else {"name": "Client", "investor_profile": "Investor profile", "email": "N/A"}
        )
        account_data = (
            {
                "balance": float(account.balance) if account.balance is not None else 0.0,
                "account_number": account.user_id,
                "blockchain": account.blockchain,
            }
            if account
            else {"balance": 0.0, "account_number": user_id, "blockchain": "N/A"}
        )
        return {**profile, **account_data}

    except Exception as e:
        print(f"[Database Neon Error - profile/account]: {e}")
        return {
            "name": "Client",
            "investor_profile": "Investor profile",
            "email": "N/A",
            "balance": 0.0,
            "account_number": user_id,
            "blockchain": "N/A",
        }
    finally:
        db.close()








