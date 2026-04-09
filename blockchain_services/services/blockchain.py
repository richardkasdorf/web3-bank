# blockchain_services/services/blockchain.py
import os
from decimal import Decimal
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

load_dotenv()

# ====================== .env Config ======================
SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
BANK_PRIVATE_KEY = os.getenv("BANK_PRIVATE_KEY")
USDC_CONTRACT = os.getenv("USDC_CONTRACT")

if not all([SEPOLIA_RPC, BANK_PRIVATE_KEY, USDC_CONTRACT]):
    raise Exception("❌ Missing .env files (SEPOLIA_RPC, BANK_PRIVATE_KEY ou USDC_CONTRACT)")

# ====================== Blockchain Connection ======================
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Hot Wallet Bank
BANK_ADDRESS = w3.eth.account.from_key(BANK_PRIVATE_KEY).address

print(f"✅ Blockchain service loaded - Bank Hot Wallet: {BANK_ADDRESS}")

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
]

usdc_contract = w3.eth.contract(address=USDC_CONTRACT, abi=ERC20_ABI)

def get_usdc_balance(address: str) -> Decimal:
    """Return balance USDC from any address"""
    try:
        balance_wei = usdc_contract.functions.balanceOf(address).call()
        return Decimal(balance_wei) / Decimal(10**6) 
    except Exception as e:
        raise Exception(f"Error checking balance USDC: {str(e)}")


def transfer_usdc(to_address: str, amount: Decimal) -> str:
    """Transfer USDC From Hot Wallet Bank to informed address"""
    if not w3.is_address(to_address):
        raise ValueError(f"Invalid address: {to_address}")

    amount_wei = int(amount * Decimal("1000000"))

    try:
        nonce = w3.eth.get_transaction_count(BANK_ADDRESS)

        tx = usdc_contract.functions.transfer(to_address, amount_wei).build_transaction({
            'chainId': 11155111,           # Sepolia
            'gas': 120000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        signed_tx = w3.eth.account.sign_transaction(tx, BANK_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_hash_hex = w3.to_hex(tx_hash)
        print(f"✅ Transaction completed: {tx_hash_hex}")
        return tx_hash_hex

    except Exception as e:
        raise Exception(f"Error transferring USDC: {str(e)}")


def get_bank_address() -> str:
    """Return Hot Wallet Bank"""
    return BANK_ADDRESS



