from circle.web3 import utils, developer_controlled_wallets
from dotenv import load_dotenv
import os
import json

load_dotenv()

CIRCLE_API_KEY = os.getenv('CIRCLE_API_KEY')
HEX_ENCODED_ENTITY_SECRET = os.getenv('CIRCLE_ENTITY_SECRET')

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
            "blockchains": ["ARC-TESTNET"],
            "count": 1,
            "accountType": "EOA"
        })
    )

    print(json.dumps(json.loads(wallet_set.model_dump_json()), indent=2))
    print(json.dumps(json.loads(wallet.model_dump_json()), indent=2))
except developer_controlled_wallets.ApiException as e:
    print("Exception when calling the Circle Wallets API: %s\n" % e)


'''
{
  "data": {
    "wallet_set": {
      "id": "c61fa248-1470-54b1-b328-c65420cc2699",
      "create_date": "2026-05-15T00:55:03Z",
      "update_date": "2026-05-15T00:55:03Z",
      "custody_type": "DEVELOPER"
    }
  }
}
{
  "data": {
    "wallets": [
      {
        "id": "cda4f5ca-2ce7-54bc-8aa6-72dbfbf7d561",
        "address": "0x1607b96ad6e2adc573d19a1f8845fd8197900982",
        "blockchain": "ARC-TESTNET",
        "create_date": "2026-05-15T00:55:03Z",
        "update_date": "2026-05-15T00:55:03Z",
        "custody_type": "DEVELOPER",
        "name": null,
        "ref_id": null,
        "state": "LIVE",
        "user_id": null,
        "wallet_set_id": "c61fa248-1470-54b1-b328-c65420cc2699",
        "initial_public_key": null,
        "account_type": "EOA"
      }
    ]
  }
}
----------------------------------------------------------------------------------------------
{
  "data": {
    "wallet_set": {
      "id": "fc2719af-9704-5204-9920-718651917e52",
      "create_date": "2026-05-15T01:09:40Z",
      "update_date": "2026-05-15T01:09:40Z",
      "custody_type": "DEVELOPER"
    }
  }
}
{
  "data": {
    "wallets": [
      {
        "id": "80fe0732-769a-5303-8991-ef8d9751bbf6",
        "address": "0xb62300e1acc8e6a0df5ecb6ede83cc967ac98687",
        "blockchain": "ARC-TESTNET",
        "create_date": "2026-05-15T01:09:40Z",
        "update_date": "2026-05-15T01:09:40Z",
        "custody_type": "DEVELOPER",
        "name": null,
        "ref_id": null,
        "state": "LIVE",
        "user_id": null,
        "wallet_set_id": "fc2719af-9704-5204-9920-718651917e52",
        "initial_public_key": null,
        "account_type": "EOA"
      }
    ]
  }
}
'''