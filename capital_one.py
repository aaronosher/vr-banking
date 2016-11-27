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

	"""
	Used to find an account.
	Searches and returns all accounts with a common search term.
	Entire search term does not need to be in the name for it to find it
	this is not the case for integer values
	"""
	def find_account(self, accounts=0, search_term=0):
		# Check if accounts is set or not. Use sef.accounts if its not
		if accounts == 0:
			accounts = self.accounts

		# Check if a search term has been set
		if search_term == 0:
			return None

		# make search_term case insesitive
		search_term = search_term.lower()

		# set results list
		results = []

		# Check if search term is a type of account
		if search_term in ['Credit Card', 'Savings', 'Checking']:
			results = self.find_multiple_accounts(account_type=search_term)

		# Otherwise just check for accoutns containing the data
		else:
			# gets a specific accoutn from the user using user_request
			logging.debug(search_term)
			for i in accounts:
				# Loop trough accounts
				for key, value in i.items():
					# Check if key is nickname so we don't run anything that cannot by done on an int type
					if key in ['nickname']:
						if search_term in value.lower():
							results.append(capitalOneAccount(i['_id']))
					# If its an int we just check for an equal value
					elif key in ['rewards', 'balance']:
						if search_term == value:
							results.append(capitalOneAccount(i['_id']))

		# if length is > 0 we return the accounts
		if len(results) > 0:
			return {'length': len(results), 'accounts': results}

		# If no accounts exists we just return length:0 – this is so there is no confuse between an actual error and just no resutls
		else:
			return {'length': 0}

	"""
	used for getting all accounts of a specific type
	returns a list of capitalOneAccount objects
	"""
	def find_multiple_accounts(self, accounts=0, account_type=0):
		# Check if accounts is set or not. Use sef.accounts if its not
		if accounts == 0:
			accounts = self.accounts

		if account_type not in ['Credit Card','Savings','Checking']:
			return "Invalid Account Type"

		results = []

		# gets all of an account type from the user using user_request
		logging.debug(account_type)
		for i in accounts:
			if account_type == i['type']:
				results.append(capitalOneAccount(i['_id']))

		return results

def get_total_balance(self):
	total = 0
	for i in self.accounts:
		if i['nickname'] == 'Credit Card':
			total = total -  i['balance']
			print(total)
		else:
			total = total + i['balance']
			print(total)
	return total

"""
name => account id
name => account name/nickname
balance => accont balance
	Note credit cards are technically negative
rewards => accounts reward balance
_type => accoutn type
	Checking, Savings, Credit Card
"""
class capitalOneAccount(capitalOne):
	#Object Vatibales
	_id = None
	name = None
	balance = None
	rewards = None
	_type = None
	customername = None

	def __init__(self, account_id):
		if account_id is None:
			return None

		self.get_account(account_id=account_id)

		return None

	def get_account(self, account_id=0):
		# Check if user_id is set or not. Use sef.user_id if its not
		if account_id is None:
			return None

		# gets the users accounts information
		url = 'http://api.reimaginebanking.com/accounts/{}/?key={}'.format(account_id, self.API_KEY)
		response = requests.get(url)
		response = json.loads(response.text)

		self._id = response['_id']
		self.name = response['nickname']
		self.balance = response['balance']
		self.rewards = response['rewards']
		self._type = response['type']
		self.customer_id = response['customer_id']


		return None

	def get_bills(self):
		bills =  []
		# gets the account's bills
		url = 'http://api.reimaginebanking.com/accounts/{}/bills?key={}'.format(self._id, self.API_KEY)
		response = requests.get(url)
		response = json.loads(response.text)

		for i in response:
			bills.append(captialOneBill(bill_id=i['_id']))

		return {'total': len(bills), 'bills': bills}

class captialOneBill(capitalOne):
	# Object variabls
	_id = None
	status = None
	payee = None
	name = None
	creation_date = None
	account_id = None
	recurring_date = None
	upcoming_account_id = None
	payment_amount = None
	account_id = None

	def __init__(self, bill_id):
		if bill_id is not None:
			self.getBiil(bill_id=bill_id)

		return None

	def getBiil(self, bill_id):
		if bill_id is None:
			return None

		# gets the bill information
		url = 'http://api.reimaginebanking.com/bills/{}/?key={}'.format(bill_id, self.API_KEY)
		response = requests.get(url)
		response = json.loads(response.text)

		self._id = response['_id']
		self.status = response['status']
		self.payee = response['payee']
		self.name = response['nickname']
		self.creation_date = response['creation_date']
		self.account_id = response['account_id']
		self.recurring_date = response['recurring_date']
		self.payment_amount = response['payment_amount']
		self.account_id = response['account_id']


user = capitalOneCustomer(user_id='583998b40fa692b34a9b8766')
print(user.find_multiple_accounts(account_type='Savings'))
