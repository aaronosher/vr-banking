import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

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


# Python functions
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


if __name__ == '__main__':

    app.run(debug=True)
