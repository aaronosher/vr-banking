import requests

class capitalOne:
	@staticmethod
	def get_user():
		url = '''http://api.reimaginebanking.com/customers/583998b40fa692b34a9b8766/accounts?key=64af502fd1accf4c465e230fc76e0327'''
		data = '{"type": "Credit Card","nickname": "Way Too High APR","rewards": 700,"balance": 0}'
		response = requests.get(url, data=data)
		return response

print(capitalOne.get_user().text)
