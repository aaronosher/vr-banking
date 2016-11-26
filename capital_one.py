import requests
import json

import logging

# imports the loggign module, creates a logging file called "ProgramLog.txt"
logging.basicConfig(filename='_ProgramLog.txt', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s- %(message)s')

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

	def parse_accounts_of_users(parsed_json, user_request):
		logging.debug(user_request)
		# gets a specific accoutn from the user using user_request


		logging.debug("parsed json is")
		for i in parsed_json:
			for key, value in i.items():
				if user_request == value:
					return i['_id']


v = {"cat" : "the defintion of a cat"}

user_account_id = '5839a4890fa692b34a9b8770'
response1 = (capitalOne.get_user().text)
#dump_json = json.dumps(response1)

parsed_json = json.loads(response1)
print(parsed_json)

print(capitalOne.parse_accounts_of_users(parsed_json, user_request='Credit Card'))