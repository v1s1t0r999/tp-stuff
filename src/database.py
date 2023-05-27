import os
import requests

_id = os.getenv('pasteid') # your pasteid
url = f'https://api.jsonbin.io/v3/b/{_id}'
headers = {
	'Content-Type': 'application/json',
	'X-Master-Key': os.getenv("pastekey") # https://jsonbin.io/app/app/api-keys
}


def read(roomname:str=None):
	con = requests.get(url, headers=headers)
	if roomname:
		try:
			return con.json()['record']['full_data'][roomname] # messages list of the "roomname"
		except KeyError: 
			add(roomname)
			newcon = requests.get(url, headers=headers)
			return newcon.json()['record']['full_data'][roomname]
	return con.json()['record']['full_data'] # json dict of all the messages


def add(roomname,data=None): # str roomname or with data
	con = read() # json dict of all the rooms
	print("____________________")
	if not data:
		con.update({roomname:[{"from": "SYSTEM","content": f"NEW CHANNEL NAMED \"{roomname.capitalize()}\"","timestamp":"00:00:00"}]})
		new = requests.put(url, json={'full_data':con}, headers=headers)
		print("++++++++++++++++++++++")
		return new.json()['record']['full_data'] # returns new complete json
	#roomname is a dict || {roomname:{["from":"user","content":"this this"]}}
	con[roomname].append(data) # Full room data is formatted with new+old content!
	print("==============================")
	new = requests.put(url, json={'full_data':con}, headers=headers)
	print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
	return new.json()['record']['full_data'] # returns new complete json


# def delete(roomname):
# 	if roomname:
# 		req = requests.put(url, json={'full_data':{}}, headers=headers)
# 	return req.json()['record'] # the full_data becomes empty, ie, without anyroom data
 
