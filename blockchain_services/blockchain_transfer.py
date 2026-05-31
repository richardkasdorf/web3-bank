from dotenv import load_dotenv
from sqlalchemy.orm import Session
from accounts.models import Account
from fastapi import HTTPException

load_dotenv()

#Singleton ou um Cache LRU para a MASTER_KEY

def resolve_destination(destination: str, db: Session) -> str:

    destination = destination.strip()
    
    if destination.startswith("0x"):
        if len(destination) != 42:
            raise HTTPException(status_code=400, detail="❌ Invalid wallet address.")
        return destination
        
    if destination.isdigit() and len(destination) == 6:
        account_destination = db.query(Account).filter(Account.user_id == int(destination)).first()
        if not account_destination:
            raise HTTPException(
                status_code=404, 
                detail= f"❌ Account '{destination}' not found."
            )
        return account_destination.wallet_address
        
    raise HTTPException(
        status_code=400, 
        detail="❌ Invalid destination. Enter a 6-digit account number or an address starting with 0x."
    )










# ====================== Services ======================
'''
SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
USDC_CONTRACT = os.getenv("USDC_CONTRACT")

w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
usdc_contract = w3.eth.contract(address=Web3.to_checksum_address(USDC_CONTRACT), abi=ERC20_ABI)

def transfer_usdc(db: Session, external_to_address: str, external_from_address: str, amount: Decimal) -> str:

    account = db.query(Account).filter(Account.wallet_address == external_from_address).first()

    if not account:
        raise ValueError("Account not found.")
    if account.balance < amount:
        raise ValueError("Insufficient internal balance.")
    if not w3.is_address(external_to_address):
        raise ValueError(f"Invalid address: {external_to_address}")

    private_key = decrypt_data()
    bank_address = w3.eth.account.from_key(private_key).address
    amount_wei = int(amount * Decimal("1000000"))

    try:

        nonce = w3.eth.get_transaction_count(bank_address)
        
        tx = usdc_contract.functions.transfer(external_to_address, amount_wei).build_transaction({
            'chainId': 11155111,
            'gas': 120000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] == 0:
            raise Exception(f"Blockchain transaction error. Hash: {w3.to_hex(tx_hash)}")
        
        new_transaction = TransactionLedger(
            from_account_id = account.user_id,
            external_to_address = external_to_address.strip(),
            amount = amount,
            type = "EXTERNAL_TRANSFER",
            tx_hash = w3.to_hex(tx_hash)
        )
        db.add(new_transaction)
        db.commit()
        return w3.to_hex(tx_hash)
        
    except Exception as e:
        db.rollback()
        raise Exception(f"Transfer error: {str(e)}")
    

if __name__ == "__main__":
    try:
        pk = decrypt_data()
    except Exception as e:
        print(f"Decrypt error: {e}")

'''





