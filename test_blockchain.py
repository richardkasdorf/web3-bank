
## CIRCLE BALANCE
import requests
url = "https://api.circle.com/v1/w3s/wallets/b31ada1b-107d-5a60-bb8f-bb9adef0b5da/balances?pageSize=10"
headers = {"Authorization": "Bearer TEST_API_KEY:7f1edf10a0446e57cc452f2c360060dc:daebac4675459409fb4c01776d7d5a05"}
response = requests.get(url, headers=headers)
print(response.text)










