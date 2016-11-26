import requests

API_KEY = '0d43177fd2d1f2a235f4222ed1cc32bd'

class capitalOne:
	@staticmethod
	def get_user():
		url = '''http://api.reimaginebanking.com/customers/583998b40fa692b34a9b8766/accounts?key={}'''.format(API_KEY)
		data = '{"type": "Credit Card","nickname": "Way Too High APR","rewards": 700,"balance": 0}'
		response = requests.get(url, data=data)
		return response
	def get_account(id):
		url = '''api.reimaginebanking.com/accounts/{}/?key={}'''.format(id, API_KEY)
		response = requests.get(url)
		return response


print(capitalOne.get_user().text)
id = ''5839a4890fa692b34a9b8770''
print(capitalOne.get_account(id))
