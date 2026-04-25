# blockchain_services/services/blockchain.py
import os, hvac
from decimal import Decimal
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

load_dotenv()

# ====================== Vault Config ======================
VAULT_URL = os.getenv("VAULT_URL", "http://localhost:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "root_token_estudo")

def get_private_key_from_vault():
    client = hvac.Client(url=VAULT_URL, token=VAULT_TOKEN)
    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path='config'
        )
        secrets = read_response['data']['data']
        return secrets
    
    except Exception as e:
        raise Exception(f"❌ Vault access error: {str(e)}")


# ====================== Blockchain Connection ======================
SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
USDC_CONTRACT = os.getenv("USDC_CONTRACT")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

if not all([SEPOLIA_RPC, USDC_CONTRACT]):
    raise Exception("❌ Ambient variables missing (SEPOLIA_RPC or USDC_CONTRACT)")

w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

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
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

usdc_contract = w3.eth.contract(address=USDC_CONTRACT, abi=ERC20_ABI)

# ====================== Services ======================

def transfer_usdc(to_address: str, amount: Decimal) -> str:
    if not w3.is_address(to_address):
        raise ValueError(f"Invalid address: {to_address}")

    private_key = get_private_key_from_vault()
    bank_address = w3.eth.account.from_key(private_key).address

    amount_wei = int(amount * Decimal("1000000"))

    try:
        nonce = w3.eth.get_transaction_count(bank_address)

        tx = usdc_contract.functions.transfer(to_address, amount_wei).build_transaction({
            'chainId': 11155111,
            'gas': 120000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt['status'] == 0:
            raise Exception(f"Blockchain transsacion error. Hash: {w3.to_hex(tx_hash)}")

        return w3.to_hex(tx_hash)

    except Exception as e:
        raise Exception(f"Transfer error: {str(e)}")



''' python -c "import blockchain; blockchain.get_bank_balance()" '''
def get_bank_balance():
    if w3.is_connected():
        print("✅ Online on Sepolia!")
    else:
        print("❌ Connection fail.")

    decimais = usdc_contract.functions.decimals().call()
    usdc_balance = usdc_contract.functions.balanceOf(PUBLIC_ADDRESS).call()
    real_balance = usdc_balance / (10 ** decimais)
    print(f"Balance: {usdc_balance}")
    print(f"Decimals: {decimais}")
    print(f"Real Balance: {real_balance} USDC")

''' python -c "import blockchain; blockchain.get_eth_balance()" '''
def get_eth_balance():
    if not w3.is_connected():
        print("❌ Conection fail.")
        return
    balance_wei = w3.eth.get_balance(PUBLIC_ADDRESS)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    print(f"Wei balance: {balance_wei}")
    print(f"Real balance: {balance_eth} ETH")
    return balance_eth





