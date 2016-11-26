import requests
import json

API_KEY = '64af502fd1accf4c465e230fc76e0327'

class capitalOne:
	@staticmethod
	def get_user():
		# Gets the users information
		url = '''http://api.reimaginebanking.com/customers/583998b40fa692b34a9b8766/accounts?key={}'''.format(API_KEY)
		data = '{"type": "Credit Card","nickname": "Way Too High APR","rewards": 700,"balance": 0}'
		response = requests.get(url, data=data)
		return response

	def get_account(user_account_id):
		# gets the users accounts information
		url = '''http://api.reimaginebanking.com/accounts/{}/?key={}'''.format(user_account_id, API_KEY)
		response = requests.get(url)
		return response

	def parse_accounts_of_users(response, user_request):
		# gets a specific accoutn from the user using user_request
		dump_json = json.dumps(response)
		parsed_json = json.loads(response)
		for i in parsed_json:
			if user_request in i:
				# if users requests is foudn in dictionary
				account_id = i['_id']
				# i is an interator going over every dictionary within json object
				return account_id


user_account_id = '5839a4890fa692b34a9b8770'
response1 = (capitalOne.get_user().text)
print(capitalOne.parse_accounts_of_users(response1, user_request='rewards'))