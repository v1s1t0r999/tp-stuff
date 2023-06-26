import os
import requests
# from flask import jsonify
import ShitDB

WOTD = "car"

db = ShitDB.DB(os.getenv("github_token"), "sources", ("v1s1t0r999", os.getenv("mail")))


def read(roomname:str = None):
    rooms = db.load_remote_data("rooms.json", eval_output=True)
    if roomname:
        try:
            return rooms[roomname]
        except KeyError:
            add(roomname)
            new_rooms = db.load_remote_data("rooms.json", eval_output=True)
            return new_rooms[roomname]
    return rooms

def read_bot(user):
	all_bots = db.load_remote_data("bot.json", eval_output=True)
	try:
		print(all_bots[user])
		return all_bots[user]
	except KeyError:
		all_bots.update({user:[{"from": "Ecstacy","content": f"Hello!","timestamp":"00:00:00","avatar":"https://tp-stuff.vercel.app/static/ecstasy.png"}]})
		db.push_remote_data(all_bots, "bot.json")
	print(all_bots)
	return all_bots[user]


def add_bot(user, data):
	user_bots = read_bot(user)
	user_bots.update(data)
	db.push_remote_data(user_bots, "bot.json")
	print(user_bots)
	return user_bots


def add(roomname, data=None):
    rooms = read()
    if not data:
        rooms.update({roomname:[{"from": "SYSTEM","content": f"NEW CHANNEL NAMED \"{roomname.capitalize()}\"","timestamp":"00:00:00","avatar":"https://tp-stuff.vercel.app/static/ecstasy.png"}]})
        db.push_remote_data(rooms,"rooms.json")
        return db.load_remote_data("rooms.json", eval_output=True)[roomname]
    
    rooms[roomname].append(data)
    db.push_remote_data(rooms, "rooms.json")
    return db.load_remote_data("rooms.json", eval_output=True)[roomname]


def get_avatar(_ip):
	con = db.load_remote_data("avatars.json", eval_output=True)
	try:
		return con['ip_avatars'][_ip]
	except KeyError:
		con['ip_avatars'].update({_ip : requests.get(f"https://loremflickr.com/json/320/320/{WOTD}").json()['file']})
		db.push_remote_data(con, "avatars.json")
		return con['ip_avatars'][_ip] # returns new complete json


def set_avatar(_ip,av):
    con = db.load_remote_data("avatars.json", eval_output=True)
    con['ip_avatars'].update({_ip : av})
    db.push_remote_data(con, "avatars.json")
    return {_ip : av}

