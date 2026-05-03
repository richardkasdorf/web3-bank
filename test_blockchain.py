

# AES-256 

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_data(data: str, secret_key: str):

    key = secret_key.encode().ljust(32)[:32] 
    aesgcm = AESGCM(key)
    nonce = os.urandom(12) 
    
    ct = aesgcm.encrypt(nonce, data.encode(), None)
    
    return nonce + ct

def decrypt_data(enveloped_data: bytes, secret_key: str):
    key = secret_key.encode().ljust(32)[:32]
    nonce = enveloped_data[:12]
    ct = enveloped_data[12:]
    
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None).decode()


master_key = "4mecu]#)8XWo+e*?"
original_test = "Chave-Privada-Da-Wallet-USDC"

encrypted = encrypt_data(original_test, master_key)
print(f"Criptografado (bytes): {encrypted.hex()}")

decrypted = decrypt_data(encrypted, master_key)
print(f"Descriptografado: {decrypted}")




















