import os
from decimal import Decimal
from blockchain_services.services.blockchain import get_private_key_from_vault, ERC20_ABI
from dotenv import load_dotenv
from web3 import Web3
from sqlalchemy.orm import Session
from accounts.models import TransactionLedger, Account

load_dotenv()

# ====================== Services ======================

SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
USDC_CONTRACT = os.getenv("USDC_CONTRACT")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
usdc_contract = w3.eth.contract(address=USDC_CONTRACT, abi=ERC20_ABI)


def transfer_usdc(db: Session, external_to_address: str, external_from_address: str, amount: Decimal) -> str:

    account = db.query(Account).filter(Account.id == external_from_address).first()

    if not account:
        raise ValueError("Account not found.")
    if account.balance < amount:
        raise ValueError("Insufficient internal balance.")

    if not w3.is_address(external_to_address):
        raise ValueError(f"Invalid address: {external_to_address}")

    private_key = get_private_key_from_vault()
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
            external_to_address = external_to_address,
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

