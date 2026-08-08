import os, json
from pathlib import Path
import requests
from db.database import get_db_session
from accounts.models import TransactionLedger, User, Account
from sqlalchemy import or_


OLLAMA_URL = os.getenv('OLLAMA_URL')
MODEL = "qwen2.5:3b"


class ChatbotService:
    def __init__(self):

        ## ----- LOCAL "STUFF" ----- ##
        BASE_DIR = Path("/app/chatbot/data")

        with open(BASE_DIR / "prompt.md", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    ## ----- DATA BASE INTEGRATION ----- ##
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
                return {"name": "Client", "investor_profile": "Investor profile", "email": "N/A"}

            return {
                "name": user.full_name,
                "email": user.email,
                "investor_profile": user.investor_profile
            }
        except Exception as e:
            print(f"[Database Neon Error - profile]: {e}")
            return {"name": "Client", "investor_profile": "Investor profile", "email": "N/A"}
        finally:
            db.close()

    def _get_user_account(self, user_id: int):
            db = get_db_session()
            try:
                account = db.query(Account).filter(Account.user_id == user_id).first()
                if not account:
                    return {"balance": 0.0, "account_number": user_id, "blockchain": "N/A"}
    
                return {
                    "balance": float(account.balance) if account.balance is not None else 0.0,
                    "account_number": account.user_id,
                    "blockchain": account.blockchain
                }
            except Exception as e:
                print(f"[Database Neon Error - profile]: {e}")
                return {"balance": 0.0, "account_number": user_id, "blockchain": "N/A"}
            finally:
                db.close()


    ## ----- AI RESPONSE ----- ##
    def generate_reply(self, user_id: int, user_message: str) -> str:
        msg = user_message.lower()

        financial_keywords = ["saldo", "balance", "transaction", "transação", "sent", "enviei",
                            "received", "recebi", "extrato", "money", "dinheiro", "valor", 
                            "perfil", "perfil de risco", "risk profile", "blockchain", "numero conta",
                            "account number"]

        needs_context = any(k in msg for k in financial_keywords)

        if needs_context:
            transactions = self._get_user_transactions(user_id)
            user_profile = self._get_user_profile(user_id)
            account = self._get_user_account(user_id)

            context = (
                f"Nome do cliente (client name): {user_profile['name']}. Perfil de investidor: {user_profile['investor_profile']}.\n"
                f"Saldo atual (balance): {account['balance']} USDC na rede {account['blockchain']}.\n"
                f"Número da conta (account number): {account['account_number']}.\n"
                f"Últimas transações (transactions): {json.dumps(transactions, ensure_ascii=False)}"
            )

        else:
            context = "No financial data needed for this message."

        prompt = f"""
        {self.system_prompt}

        CLIENT CONTEXT:
        {context}

        Message: {msg}
        """

        try:
            a = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=120)
            a.raise_for_status()
            return a.json().get('response', "Sorry, I couldn't generate a response.")
        except requests.exceptions.RequestException as e:
            print(f"[Ollama Error]: {e}")
            return "Sorry, i don't know the answer for your question. But i'm in constantly training."

