# blockchain_services/services/blockchain.py
import os
import hvac
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
            mount_point='secret', 
            path='bank-secrets'
        )
        return read_response['data']['data']['private_key']
    except Exception as e:
        raise Exception(f"❌ Vault access error: {str(e)}")


# ====================== Blockchain Connection ======================
SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
USDC_CONTRACT = os.getenv("USDC_CONTRACT")

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
    }
]

usdc_contract = w3.eth.contract(address=USDC_CONTRACT, abi=ERC20_ABI)

# ====================== Funções de Serviço ======================

def transfer_usdc(to_address: str, amount: Decimal) -> str:
    if not w3.is_address(to_address):
        raise ValueError(f"Endereço inválido: {to_address}")

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

        return w3.to_hex(tx_hash)

    except Exception as e:
        raise Exception(f"Erro ao transferir USDC: {str(e)}")

def get_bank_address() -> str:
    pk = get_private_key_from_vault()
    return w3.eth.account.from_key(pk).address




