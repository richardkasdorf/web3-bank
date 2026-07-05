
''' ## CIRCLE BALANCE
import requests
url = "https://api.circle.com/v1/w3s/wallets/0fc630be-72e4-552b-a905-642682a7f133/balances?pageSize=10"
headers = {"Authorization": "Bearer TEST_API_KEY:7f1edf10a0446e57cc452f2c360060dc:daebac4675459409fb4c01776d7d5a05"}
response = requests.get(url, headers=headers)
print(response.text)
'''









