import os
import requests

_id = os.getenv('pasteid') # your pasteid
url = f'https://api.jsonbin.io/v3/b/{_id}'
headers = {
	'Content-Type': 'application/json',
	'X-Master-Key': os.getenv("pastekey") # https://jsonbin.io/app/app/api-keys
}


def read():
	con = requests.get(url, headers=headers)
	return con.json()['record']['messages'] # list of all the messages


def add(data):
	con = read()
	con.append(data)
	new = requests.put(url, json={'messages':con}, headers=headers)
	return new.json()['record'] # appends message data to the list


def delete():
	req = requests.put(url, json={'messages':[]}, headers=headers)
	return req.json()['record'] # the list become empty
 
