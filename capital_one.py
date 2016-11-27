import requests
import json

import logging

# imports the loggign module, creates a logging file called "ProgramLog.txt"
logging.basicConfig(filename='_ProgramLog.txt', level=logging.DEBUG,
					format=' %(asctime)s - %(levelname)s- %(message)s')


class capitalOne:
	#API key
	API_KEY = '64af502fd1accf4c465e230fc76e0327'
	GLOBAL_PAYEE = '583a92c80fa692b34a9b89e8'



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
			print("[===] Results:",results)
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
		print("[===] Account type:",account_type)
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

	def get_bills(self):
		bills = []
		# gets the account's bills
		url = 'http://api.reimaginebanking.com/accounts/{}/bills?key={}'.format(self._id, self.API_KEY)
		response = requests.get(url)
		response = json.loads(response.text)

		for i in response:
			bills.append(capitalOneBill(bill_id=i['_id']))

			return {'total': len(bills), 'bills': bills}


class capitalOneBill(capitalOne):
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
		self.payment_amount = response['payment_amount']
		self.account_id = response['account_id']

	def pay(self):
		if self.status == 'completed':
			return {"errors": "Bill is Already Paid"}

		elif self.status == 'canceled':
			return {"errors": "Bill has been canceled"}

		if capitalOneTransfer.new(_from=self.account_id, _to=self.GLOBAL_PAYEE, amount=self.payment_amount, API_KEY=self.API_KEY)._id is not None:
			self.markAsPaid()
			return {"errors": "None", status: "Bill is Paid"}

	def markAsPaid(self):
		url = 'http://api.reimaginebanking.com/bills/{}/?key={}'.format(self._id, self.API_KEY)
		data = {"status": "completed"}
		headers = {'content-type':'application/json'}
		response = requests.put(url, data=json.dumps(data), headers=headers)

class capitalOneTransfer(capitalOne):
	_id = None
	_type = None
	transaction_date = None
	status = None
	medium = None
	payer_id = None
	payee_id = None
	amount = None
	description = None

	def __init__(self, transfer_id):
		if transfer_id is None:
			return None

		self.get(transfer_id=transfer_id)

		return None


	def get(self, transfer_id):
		if transfer_id is None:
			return False

		url = 'http://api.reimaginebanking.com/transfers/{}/?key={}'.format(transfer_id, self.API_KEY)
		response = requests.get(url)
		response = json.loads(response.text)

		print(response)

		self._id = response['_id']
		self._type = response['type']
		self.status = response['status']
		self.medium = response['medium']
		self.payer_id = response['payer_id']
		self.payee_id = response['payee_id']
		self.amount = response['amount']

		return None

	@staticmethod
	def new(_from, _to, amount, API_KEY):
		data = {"medium": "balance", "payee_id": _to, "amount": amount}
		url = 'http://api.reimaginebanking.com/accounts/{}/transfers/?key={}'.format(_from, API_KEY)
		headers = {'content-type':'application/json'}
		response = requests.post(url, data=json.dumps(data), headers=headers)
		response = json.loads(response.text)

		if response["objectCreated"]["_id"] is not None:
			return capitalOneTransfer(transfer_id=response["objectCreated"]["_id"])

		return None



class capitalOnePayment(capitalOne):

	def __init__(self):
		return None

	def pay(self, amount, account, merchant_id='57cf75cea73e494d8675ec49'):
		try:
			amount = float(amount)
		except TypeError as e:
			print("Amount is not a number.")
			return 1

		data = {"merchant_id": "57cf75cea73e494d8675ec49","medium": "balance","purchase_date": "2016-11-27","amount": amount,"description": ""}

		url = 'http://api.reimaginebanking.com/merchants?key={}&id={}'.format(self.API_KEY, '5839a79a0fa692b34a9b8771')
		r = requests.post(url, data)
		print(r)
		print(r.text)
		if r == """"<Response [200]>""":
			print(r.text)
		else:
			return False


	def owe_money(self, how_much):
		# this may not work for names with numbers in
		import os
		import json

		# assuming how_much is a dictionary
		if os.path.exists("owe.json"):
			file = open("owe.json", 'r+')
			data = json.load(file)

			key = how_much[0]
			value = how_much[1]

			data[key] = value

			file.close()
			file = open("owe.json", 'w')
			json.dump(data, fp=file)
			file.close()
		else:
			# this literally doesnt work
			file = open("owe.json", 'w')
			how_much = list(how_much)
			a = json.dump(how_much)
			file.write(a)
			file.close()

	def how_much_do_i_owe(self):
		with open("owe.json", 'r') as fp:
			return json.load(fp)

	def getPayment(self, bill_id):
		if bill_id is None:
			return None
		# whats bill ID

		# gets the bill information
		data = {"merchant_id": "57cf75cea73e494d8675ec4a", "medium": "balance", "purchase_date": "2016-11-27", "amount": amount, "description": "product"}
		url = 'http://api.reimaginebanking.com/merchants?key={}&id={}'.format(self.API_KEY, account)

		r = requests.post(url, data)
		print(r)
		# we literally dont need json here, just a true or false code

class summary(capitalOne):

	def __init__(self):
		return None

	def summary(self):
		# Financial summart
		object = capitalOnePayment()
		owe = object.how_much_do_i_owe(self)
		total = get_total_balance(self)
		object = capitalOneCustomer(self)
		total = object.get_total_balance()

		length = len(owe)
		string = ""
		for key, value in owe.items():
			string = string + "{} {} pounds".format(key, value)
		everything = "You currently have a networth of {}. You owe {}".format(total, string)


user = capitalOneCustomer(user_id='583998b40fa692b34a9b8766')

print(user.find_account(search_term='ben checking')['accounts'][0].get_bills())
#
# bill = capitalOneBill(bill_id='583ab6850fa692b34a9b8a06')
#
# print(bill.pay())
