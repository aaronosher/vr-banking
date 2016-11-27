import random
import pickle
import os.path
import json

#TODO test this

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


