import requests
import json

customerId = '583998b40fa692b34a9b8766'
apiKey = '64af502fd1accf4c465e230fc76e0327'

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
payload = {
  "type": "Checking",
  "nickname": "Made with Python2",
  "rewards": 10000,
  "balance": 10000,
}
# Create a Savings Account
response = requests.post(
	url,
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

if response.status_code == 201:
	print('account created')
