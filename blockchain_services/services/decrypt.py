import os, hvac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv
from db.database import SessionLocal
from accounts.models import Bank

load_dotenv()

VAULT_URL = os.getenv("VAULT_URL", "http://localhost:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "root_token_estudo")

# ====================== Vault Config ======================
def get_master_key_from_vault():
    client = hvac.Client(url = VAULT_URL, token = VAULT_TOKEN)
    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path = 'config',
            raise_on_deleted_version = True 
        )
        secrets = read_response['data']['data']
        print(secrets)
        return secrets['secretkey']
        
    except Exception as e:
        raise Exception(f"❌ Vault access error: {str(e)}")


def decrypt_data():
    db = SessionLocal()
    try:

        bank_record = db.query(Bank).order_by(Bank.id.desc()).first()
        if not bank_record or not bank_record.bank_assign_key:
            print("Nothing here.")
            return
        
        master_key = get_master_key_from_vault()
        if isinstance(master_key, str):
            master_key = master_key.encode()

        blob = bank_record.bank_assign_key

        key = get_master_key_from_vault().encode().ljust(32)[:32]
        aesgcm = AESGCM(key)

        nonce = blob[:12]
        ciphertext = blob[12:]

        decrypted_key = aesgcm.decrypt(nonce, ciphertext, None)
        private_key = "0x" + decrypted_key.decode().strip()

        print(private_key)
        return private_key

    except Exception as e:
        print(f"\nDecrypt Error: {e}")
        print("Maybe you must verify the Master Key")
    finally:
        db.close()



