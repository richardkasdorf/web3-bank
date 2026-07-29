import os, json, pandas as pd
from pathlib import Path
import requests
from db.database import get_db, get_db_session
from accounts.models import TransactionLedger, User
from sqlalchemy import or_


OLLAMA_URL = os.getenv('OLLAMA_URL')
MODEL = "qwen2.5:3b"


class ChatbotService:
    def __init__(self):

        ## ----- LOCAL "STUFF" ----- ##
        BASE_DIR = Path("/app/chatbot/data")

        with open(BASE_DIR / "prompt.md", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()


    def _get_user_transactions(self, user_id: int, limit: int = 5):
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


    def _get_user_profile(self, user_id: int):
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"name": "Client", "email": "N/A"}

            return {
                "name": user.full_name,
                "email": user.email
            }
        except Exception as e:
            print(f"[Database Neon Error - profile]: {e}")
            return {"name": "Client", "email": "N/A"}
        finally:
            db.close()


    def generate_reply(self, id: int, user_message: str) -> str:

        msg = user_message.lower()

        ## ----- GET DATA ----- ##
        transactions = self._get_user_transactions(id)
        user_profile = self._get_user_profile(id)

        ## ----- CONTEXT ----- ##
        context = f"""
        CLIENT: {user_profile['name']} 
        LAST TRANSACTIONS: {json.dumps(transactions, ensure_ascii=False)}
        """

        prompt = f"""
        {self.system_prompt}

        CLIENT CONTEXT:
        {context}

        Answer: {msg}
        """

        try:
            a = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=120)
            a.raise_for_status()
            return a.json().get('response', 'Sorry, cant help you at this moment.')
        except requests.exceptions.RequestException as e:
            print(f"[Ollama Error]: {e}")
            return "Sorry, i don't know the answer for your question. But i'm in constantly training."
        






