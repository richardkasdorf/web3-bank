# blockchain_services/services/blockchain.py
import os, json
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from accounts.models import Account
from db.database import SessionLocal
from pathlib import Path
import requests

load_dotenv()

# ====================== Blockchain + Neon Connection ======================
SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
USDC_CONTRACT = os.getenv("USDC_CONTRACT")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")


w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

abi_path = Path("blockchain_services/contracts/abi/usdc.json")
with open(abi_path, "r") as f:
    ERC20_ABI = json.load(f)

# Necessário instanciar a classe!!
# python -c "from blockchain_services.services.wallet_ledger_reconciliation import LedgerReconciliation; auditor = LedgerReconciliation(); auditor.fetch_blockchain_balance(); auditor.fetch_neon_balance()"
class LedgerReconciliation:
    def __init__(self):
        print("🔌 NEON + Blockchain started, loading data... \n")

    def fetch_blockchain_balance(self, wallet_address="0x547807B5912A3e804b5823F31221165D23BA72f6") -> float:
        print("🔒 Balance SEPOLIA TESTNET: ")
        usdc_contract = w3.eth.contract(address=USDC_CONTRACT, abi=ERC20_ABI)

        if w3.is_connected():
            print("Online on Sepolia ✅")
        else:
            print("❌ Connection fail.")

        decimais = usdc_contract.functions.decimals().call()
        usdc_balance = usdc_contract.functions.balanceOf(wallet_address).call()
        real_balance = usdc_balance / (10 ** decimais)
        print(f"Balance: {usdc_balance} | Real Balance: {real_balance} USDC") 
        balance_wei = w3.eth.get_balance(wallet_address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        print(f"Wei ETH balance: {balance_wei} | Real ETH balance:  {balance_eth} ETH")
        return (float(real_balance), float(balance_eth))


    def fetch_neon_balance(self, blockchain_usdc: float, blockchain_eth: float, user_id=391098) -> float:
        print("\n💲 Balance NEON Database: ")
        
        db = SessionLocal()
        try:
            account = db.query(Account).filter(Account.user_id == user_id).first()
            
            if not account:
                print(f"❌ User {user_id} not found in database.")
                return 0.0

            bank_balance = float(account.balance) if account.balance is not None else 0.0
            bank_eth_balance = float(account.eth_balance) if account.eth_balance is not None else 0.0
            print(f"Current Balance in Neon: {bank_balance:.6f} USDC | {bank_eth_balance:.18f} ETH")

            if bank_balance != blockchain_usdc or bank_eth_balance != blockchain_eth:
                print(f"🚨 Divergence detected! Changing Neon balance: {bank_balance:.6f} -> {blockchain_usdc:.6f} USDC")
                print(f"🚨 Divergence detected! Changing Neon balance: {bank_eth_balance:.18f} -> {blockchain_eth:.18f} ETH")
                
                account.balance = blockchain_usdc
                account.eth_balance = blockchain_eth
                db.commit()
                print("✅ Neon database updated successfully with blockchain balance!")
                
                bank_balance = blockchain_usdc
                bank_eth_balance = blockchain_eth
            else:
                print("🟢 Balance matches! No changes needed.")

        except Exception as e:
            db.rollback()
            print(f"[Database Neon Error]: {e}")
        
        finally:
            db.close()
            print("🔌 Database connection closed.")
            return bank_balance

    def equalizer_balance(self, wallet_address="0x547807B5912A3e804b5823F31221165D23BA72f6", user_id=391098):
        usdc_on_chain, eth_on_chain = self.fetch_blockchain_balance(wallet_address)
        
        self.fetch_neon_balance(blockchain_usdc=usdc_on_chain, blockchain_eth=eth_on_chain, user_id=user_id)

        url = "https://api.etherscan.io/v2/api?module=stats&action=ethprice&apikey=Y33NN4517KHUYXKCCPIHFWPJTNVDM2FW88&chainid=1"

        response = requests.get(url)

        print(response.text)






