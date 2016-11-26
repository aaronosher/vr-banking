import requests

API_KEY = '64af502fd1accf4c465e230fc76e0327'

class capitalOne:
	@staticmethod
	def get_user():
		url = '''http://api.reimaginebanking.com/customers/583998b40fa692b34a9b8766/accounts?key={}'''.format(API_KEY)
		data = '{"type": "Credit Card","nickname": "Way Too High APR","rewards": 700,"balance": 0}'
		response = requests.get(url, data=data)
		return response

	def get_account(user_account_id):
		url = '''http://api.reimaginebanking.com/accounts/{}/?key={}'''.format(user_account_id, API_KEY)
		response = requests.get(url)
		return response

user_account_id = '5839a4890fa692b34a9b8770'
print(capitalOne.get_account(user_account_id).text)
