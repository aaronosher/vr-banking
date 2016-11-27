import requests
import json

def jokes_alexa():
	r = requests.get("http://api.icndb.com/jokes/random")
	json1_data = json.loads(r.text)
	print(json1_data['value']['joke'])