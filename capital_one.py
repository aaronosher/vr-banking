import requests
import json

import logging

# imports the loggign module, creates a logging file called "ProgramLog.txt"
logging.basicConfig(filename='_ProgramLog.txt', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s- %(message)s')

class capitalOne:
	#API key
	API_KEY = '64af502fd1accf4c465e230fc76e0327'

class capitalOneCustomer(capitalOne):

	# Object Variables
	user_id = None
	accounts = []

	# __init__ constructor
	# Checks if user_id is valid and then saves it to the variabls
	def __init__(self, user_id):
		if user_id is None:
			return None
		if self.get_customer(user_id).status_code == 200:
			self.user_id = user_id
			self.get_accounts(user_id=user_id)

		return None

	def get_customer(self, user_id=0):
		# Check if user_id is set or not. Use sef.user_id if its not
		if not user_id:
			user_id = self.user_id

		# Make request
		url = 'http://api.reimaginebanking.com/customers/{}?key={}'.format(user_id, self.API_KEY)
		response = requests.get(url)

		return response

	def get_accounts(self, user_id=0):
		# Check if user_id is set or not. Use sef.user_id if its not
		if user_id == 0:
			user_id = self.user_id

		# Make request
		url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(user_id, self.API_KEY)
		response = requests.get(url)
		self.accounts = json.loads(response.text)

		return response

	def get_account(self, account_id=0):
		# Check if user_id is set or not. Use sef.user_id if its not
		if  account_id == 0:
			return None

		# gets the users accounts information
		url = '''http://api.reimaginebanking.com/accounts/{}/?key={}'''.format(account_id, self.API_KEY)
		response = requests.get(url)

		return response

	def search_accounts(self, accounts=0, search_term=0):
		# Check if accounts is set or not. Use sef.accounts if its not
		if accounts == 0:
			accounts = self.accounts

		if search_term == 0:
			return None

		# gets a specific accoutn from the user using user_request
		logging.debug(search_term)
		for i in accounts:
			for key, value in i.items():
				if search_term == value:
					return i['_id']

	def get_useful_information(self, account_id):
		# uses account ID to get useful information. Account ID is found by using parse_accounts_of_users
		# to find a specific account based on the search term, 'credit card' or 'savings'.
		# use get_account to get a list of multiple accounts which goes into parse_accounts
		output = requests.get('http://api.reimaginebanking.com/accounts/{}?key={}'.format(account_id, self.API_KEY))
		parsed_json = json.loads(output.text)
		name = parsed_json['nickname']
		balance = parsed_json['balance']
		if parsed_json['type'] == 'Credit Card':
			rewards = parsed_json['rewards']
			useful_dict = {"Name" : name, "Balance" : balance, "Rewards" : rewards}
		else:
			useful_dict = {"Name": name, "Balance": balance}

		return useful_dict

class capitalOneAccount(capitalOne):

	def __init__(self, account_id):
		return None

user = capitalOneCustomer(user_id='583998b40fa692b34a9b8766')

account = user.search_accounts(search_term='Savings')

print(user.get_useful_information(account_id=account))
