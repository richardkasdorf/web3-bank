from circle.web3 import utils, developer_controlled_wallets
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()

CIRCLE_API_KEY = os.getenv('CIRCLE_API_KEY')
HEX_ENCODED_ENTITY_SECRET = os.getenv('CIRCLE_ENTITY_SECRET')

def new_wallet():
    client = utils.init_developer_controlled_wallets_client(
        api_key=os.getenv("CIRCLE_API_KEY"),
        entity_secret=os.getenv("HEX_ENCODED_ENTITY_SECRET")
    )

    wallet_sets_api = developer_controlled_wallets.WalletSetsApi(client)
    wallets_api = developer_controlled_wallets.WalletsApi(client)

    try:
        wallet_set = wallet_sets_api.create_wallet_set(
            developer_controlled_wallets.CreateWalletSetRequest.from_dict({
                "name": "My First Dev-Controlled Wallet Set"
            })
        )

        wallet_set_data = wallet_set.data.wallet_set.actual_instance

        wallet = wallets_api.create_wallet(
            developer_controlled_wallets.CreateWalletRequest.from_dict({
                "walletSetId": wallet_set_data.id,
                "blockchains": ["ETH-SEPOLIA"],
                "count": 1,
                "accountType": "EOA"
            })
        )

        wallet_data = wallet.data.wallets[0].actual_instance

        return {
            "circle_wallet_id": wallet_data.id,
            "circle_wallet_set_id": wallet_data.wallet_set_id,
            "wallet_address": wallet_data.address,
            "blockchain": wallet_data.blockchain,
            "account_type": wallet_data.account_type,
            "custody_type": wallet_set_data.custody_type,
            "circle_create_date": wallet_data.create_date
        }

    except developer_controlled_wallets.ApiException as e:
        print("Exception when calling the Circle Wallets API: %s\n" % e)
        raise HTTPException(status_code=502, detail="❌ Failed to create wallet on Circle.")


'''
def new_wallet():

    client = utils.init_developer_controlled_wallets_client(
        api_key=os.getenv("CIRCLE_API_KEY"),
        entity_secret=os.getenv("HEX_ENCODED_ENTITY_SECRET")
    )

    wallet_sets_api = developer_controlled_wallets.WalletSetsApi(client)
    wallets_api = developer_controlled_wallets.WalletsApi(client)

    try:
        wallet_set = wallet_sets_api.create_wallet_set(
            developer_controlled_wallets.CreateWalletSetRequest.from_dict({
                "name": "My First Dev-Controlled Wallet Set"
            })
        )

        wallet = wallets_api.create_wallet(
            developer_controlled_wallets.CreateWalletRequest.from_dict({
                "walletSetId": wallet_set.data.wallet_set.actual_instance.id,
                "blockchains": ["ETH-SEPOLIA"],
                "count": 1,
                "accountType": "EOA"
            })
        )

        print(json.dumps(json.loads(wallet_set.model_dump_json()), indent=2))
        print(json.dumps(json.loads(wallet.model_dump_json()), indent=2))
    except developer_controlled_wallets.ApiException as e:
        print("Exception when calling the Circle Wallets API: %s\n" % e)
'''