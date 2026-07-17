import os, json, pandas as pd
from pathlib import Path
from openai import OpenAI
from db.database import get_db 
from accounts.models import TransactionLedger


class ChatbotService:
    def __init__(self):
        self.system = "Message for OpenAI, not used for now!"
        
        from pathlib import Path

        BASE_DIR = Path("/app/chatbot/data")
        
        history_path = BASE_DIR / 'history_chat.csv'
        profile_path = BASE_DIR / 'risk_profile.json'
        invest_options_path = BASE_DIR / 'invest_options.json'

        self.history_chat = pd.read_csv(history_path) if history_path.exists() else pd.DataFrame()
        #self.profile = json.load(open(profile_path, encoding='utf-8')) if profile_path.exists() else {}
        self.invest_options = json.load(open(invest_options_path, encoding='utf-8')) if invest_options_path.exists() else []

    def _get_user_transactions(self, limit: int = 5):
        db = get_db()
        try:
            transactions = db.query(TransactionLedger).order_by(TransactionLedger.id.desc()).limit(limit).all()
            tx_list = []
            for tx in transactions:
                tx_list.append({
                    "hash": tx.tx_hash,
                    "tipo": tx.type,
                    "valor": tx.amount if hasattr(tx, 'amount') else "N/A",
                    "data": tx.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(tx, 'created_at') else "N/A"
                })
            return tx_list
        except Exception as e:
            print(f"[Database Neon Error]: {e}")
            return []
        finally:
            db.close() 


    def generate_reply(self, user_message: str) -> str:
        msg = user_message.lower()
        
        if any(k in msg for k in ["Blockchain", "Withdrawal", "Crypto", "Gas", "Deposit"]):
            return json.dumps(self.history_chat, ensure_ascii=False, indent=2)
            
        if any(k in msg for k in ["invest", "application", "investment"]):
            return json.dumps(self.invest_options, ensure_ascii=False, indent=2)
        
        # Useless for now
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": self.system}, {"role": "user", "content": user_message}],
            temperature=0.7, max_tokens=250
        )
        return res.choices[0].message.content

