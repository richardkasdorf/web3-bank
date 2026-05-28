from circle.web3 import utils, developer_controlled_wallets
from dotenv import load_dotenv
import os
import time
import json

load_dotenv()

# Set transfer inputs
SOURCE_WALLET_ADDRESS = "YOUR_SOURCE_WALLET_ADDRESS"
SOURCE_WALLET_BLOCKCHAIN = "ARC-TESTNET"
DESTINATION_WALLET_ID = "YOUR_DESTINATION_WALLET_ID"
DESTINATION_WALLET_ADDRESS = "YOUR_DESTINATION_WALLET_ADDRESS"
ARC_TESTNET_USDC = "0x3600000000000000000000000000000000000000"
TRANSFER_AMOUNT_USDC = "5"

# Initialize the wallets client
client = utils.init_developer_controlled_wallets_client(
    api_key=os.getenv("CIRCLE_API_KEY"),
    entity_secret=os.getenv("CIRCLE_ENTITY_SECRET")
)

transactions_api = developer_controlled_wallets.TransactionsApi(client)
wallets_api = developer_controlled_wallets.WalletsApi(client)

# Validate the wallet inputs
if (
    SOURCE_WALLET_ADDRESS == "YOUR_SOURCE_WALLET_ADDRESS"
    or DESTINATION_WALLET_ID == "YOUR_DESTINATION_WALLET_ID"
    or DESTINATION_WALLET_ADDRESS == "YOUR_DESTINATION_WALLET_ADDRESS"
):
    raise ValueError(
        "Replace the wallet constants at the top of send_tokens.py before running the script."
    )

try:
    # Create the transfer transaction
    request = developer_controlled_wallets.CreateTransferTransactionForDeveloperRequest.from_dict({
        "walletAddress": SOURCE_WALLET_ADDRESS,
        "blockchain": SOURCE_WALLET_BLOCKCHAIN,
        "destinationAddress": DESTINATION_WALLET_ADDRESS,
        "tokenAddress": ARC_TESTNET_USDC,
        "amounts": [TRANSFER_AMOUNT_USDC],
        "feeLevel": "MEDIUM"
    })

    transfer_response = transactions_api.create_developer_transaction_transfer(request)
    transfer_data = transfer_response.data.to_dict()
    transaction_id = transfer_data["id"]
    current_state = transfer_data["state"]

    print(json.dumps(json.loads(transfer_response.model_dump_json()), indent=2))

    # Wait for the transfer to finish
    terminal_states = {"COMPLETE", "FAILED", "CANCELLED", "DENIED"}

    while current_state not in terminal_states:
        time.sleep(3)
        poll_response = transactions_api.get_transaction(id=transaction_id)
        transaction = poll_response.data.to_dict()["transaction"]
        current_state = transaction["state"]
        print(json.dumps(json.loads(poll_response.model_dump_json()), indent=2))

    if current_state != "COMPLETE":
        raise RuntimeError(f"Transaction ended in state: {current_state}")

    # Check the recipient balance
    destination_balance_response = wallets_api.list_wallet_balance(id=DESTINATION_WALLET_ID)
    print(json.dumps(json.loads(destination_balance_response.model_dump_json()), indent=2))
except developer_controlled_wallets.ApiException as e:
    print("Exception when calling the Circle Wallets API: %s\n" % e)







