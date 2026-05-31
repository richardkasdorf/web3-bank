import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv
from accounts.models import Bank
from db.database import SessionLocal

load_dotenv()

MASTER_KEY = os.getenv('MASTER_KEY')
HEX_ENCODED_ENTITY_SECRET = os.getenv('HEX_ENCODED_ENTITY_SECRET') 

def encrypt_data():

    db = SessionLocal()
    
    with SessionLocal() as db:

        try:
            key = MASTER_KEY.encode().ljust(32)[:32]
            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            
            ct = aesgcm.encrypt(nonce, HEX_ENCODED_ENTITY_SECRET.encode(), None)
            blob_final = nonce + ct

            new_bank_entry = Bank(bank_assign_key=blob_final)
            db.add(new_bank_entry)
            db.commit()
        except Exception as e:
            db.rollback() 
            print(f"Error: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    encrypt_data()


