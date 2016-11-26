import requests
import json

import logging

# imports the loggign module, creates a logging file called "ProgramLog.txt"
logging.basicConfig(filename='_ProgramLog.txt', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s- %(message)s')

API_KEY = '64af502fd1accf4c465e230fc76e0327'

class capitalOne:
	# Object Variables
	user_id = None
	accounts = []

	# __init__ constructor
	# Checks if user_id is valid and then saves it to the variabls
	def __init__(self, user_id):
		if user_id is None:
			print 'None'

		if self.get_customer(user_id).status_code == 200:
			self.user_id = user_id

		return None

	def get_customer(self, user_id=0):
		# Check if user_id is set or not. Use sef.user_id if its not
		if not user_id:
			user_id = self.user_id

		# Make request
		url = 'http://api.reimaginebanking.com/customers/{}?key={}'.format(user_id, API_KEY)
		response = requests.get(url)

		return response

	def get_accounts(self, user_id=0):
		# Check if user_id is set or not. Use sef.user_id if its not
		if not user_id:
			user_id = self.user_id

		# Make request
		url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(user_id, API_KEY)
		response = requests.get(url)

		return response

	@staticmethod
	def get_account(user_account_id):
		# gets the users accounts information
		url = '''http://api.reimaginebanking.com/accounts/{}/?key={}'''.format(user_account_id, API_KEY)
		response = requests.get(url)
		return response

	def parse_accounts_of_users(response, user_request):
		parsed_json = json.loads(response)
		# gets a specific accoutn from the user using user_request
		logging.debug(user_request)
		for i in parsed_json:
			for key, value in i.items():
				if user_request == value:
					return i['_id']

<<<<<<< HEAD
	def useful_information_account(id):
		output = requests.get('http://api.reimaginebanking.com/accounts/{}?key={}'.format(id, API_KEY))
		parsed_json = json.loads(output.text)
		print(parsed_json)
		name = parsed_json['nickname']
		balance = parsed_json['balance']
		if parsed_json[type] == 'Credit Card':
			rewards = parsed_json['rewards']
			useful_dict = {"Name" : name, "Balance" : balance, "Rewards" : rewards}
		else:
			useful_dict = {"Name": name, "Balance": balance,}

capitalOne.useful_information_account('5839a4890fa692b34a9b8770')
=======

user = capitalOne('583998b40fa692b34a9b8766')
>>>>>>> 5efc1dd32d0226152ee5601f77f0930338c2965a
