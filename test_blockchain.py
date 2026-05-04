import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv
from db.database import SessionLocal
from accounts.models import Bank

load_dotenv()

MASTER_KEY = os.getenv('MASTER_KEY')

def test_decrypt_key():
    db = SessionLocal()
    try:
        bank_record = db.query(Bank).order_by(Bank.id.desc()).first()

        if not bank_record or not bank_record.bank_assign_key:
            print("Nothing here.")
            return

        print(f"--- Database recovered (ID: {bank_record.id}) ---")
        blob = bank_record.bank_assign_key
        print(f"Binary Blob (Hex): {blob.hex()[:30]}...")

        key = MASTER_KEY.encode().ljust(32)[:32]
        aesgcm = AESGCM(key)

        nonce = blob[:12]
        ciphertext = blob[12:]

        decrypted_key = aesgcm.decrypt(nonce, ciphertext, None)
        
        print(f"Original Key: {decrypted_key.decode()}")
        
    except Exception as e:
        print(f"\nDecrypt Error: {e}")
        print("Maybe you must verify the Master Key")
    finally:
        db.close()

if __name__ == "__main__":
    test_decrypt_key()
