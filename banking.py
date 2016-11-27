import logging, capital_one
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from capital_one import capitalOneAccount, capitalOneCustomer, user
import os.path
import json
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Startup launch command
@ask.launch
def launch():
	return statement("Minions assemble")

# Intent for whenever hello is said (See utters)
@ask.intent("HelloIntent")
def hello():
	return statement("I welcome you minion")


# Stop intent
@ask.intent("AMAZON.StopIntent")
def stop():
	return statement("Exiting program")


# Session ended console output
@ask.session_ended
def sessionEnded():
	log.debug("Session ended")
	return "", 200

# Responds to given request from user input
@ask.intent("GetFirstName")
def getRequest(first_name):
	msg = "Your name is {}".format(first_name)
	return statement(msg)

@ask.intent("GetAccInfo")
def getInfo(request):
	inputRequest = str(request.title())
	print("Input Request: ", inputRequest) # Debugging only
	if  (user.search_accounts(search_term = inputRequest)) == None:
		msg = "I am sorry, I did not understand"
	else:
		accountID = user.search_accounts(search_term = inputRequest)
		account = capitalOneAccount(account_id = accountID)
		msg = "Account {0}. Your balance is {1} pounds".format(account.name, account.balance)
	return statement(msg)

@ask.intent("GetAccBal")
def getBal(request):
	inputRequest = str(request.title())
	print("Input Request: ", inputRequest) #Debugging only
	if  (user.search_accounts(search_term = inputRequest)) == None:
		msg = "I am sorry, I did not understand"
	else:
		accountID = user.search_accounts(search_term = inputRequest)
		account = capitalOneAccount(account_id = accountID)
		msg = "Your balance is {} pounds".format(account.balance)
	return statement(msg)

@ask.intent("GetAccType")
def getType(request):
	inputRequest = str(request.title())
	print("Input Request: ", inputRequest) #Debugging only
	if  (user.search_accounts(search_term = inputRequest)) == None:
		msg = "I am sorry, I did not understand"
	else:
		accountID = user.search_accounts(search_term = inputRequest)
		account = capitalOneAccount(account_id = accountID)
		msg = "Account type is {}".format(account._type)
	return statement(msg)



def owe_money(how_much):
	# assuming how_much is a dictionary
	if os.path.exists("owe.json"):
		with open("owe.json", 'r+') as fp:
			data = json.load(fp)
			data.append(how_much)
			with open("owe.json", 'w') as fp:
				json.dump(how_much, fp)
	else:
		with open("owe.json", 'w') as fp:
			json.dump(how_much, fp)

def how_much_do_i_owe():
	with open("owe.json", 'r') as fp:
		return json.load('owe.json', fp)

#@ask.intent("GetAccountID")
#def getID():
#	accDict = user.useful_information_account(id='5839a4890fa692b34a9b8770')
#	user.parse_accounts_of_users(user.get_account("5839a4890fa692b34a9b8770"), userRequest)
#	msg = "Account name " + accDict["nickname"] + " account balance " + accDict["balance"]
#	return statement(msg)

if __name__ == '__main__':
	app.run()


