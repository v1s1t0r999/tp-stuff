import os
import requests
# from flask import jsonify
import ShitDB

WOTD = "life"

db = ShitDB.DB(os.getenv("github_token"), "tp-stuff", ("v1s1t0r999", os.getenv("mail")), branch="database")


def read(roomname:str = None):
    rooms = db.load_remote_data("rooms.json", eval_output=True, branch="database")
    if roomname:
        try:
            return rooms[roomname]
        except KeyError:
            add(roomname)
            new_rooms = db.load_remote_data("rooms.json", eval_output=True, branch="database")
            return new_rooms[roomname]
    return rooms


def add(roomname, data=None):
    rooms = read()
    if not data:
        con = {roomname:[{"from": "SYSTEM","content": f"NEW CHANNEL NAMED \"{roomname.upper()}\"","timestamp":"00:00:00","avatar":"https://tp-stuff.vercel.app/static/ecstasy.png"}]}
        db.push_remote_data(con,"rooms.json", branch="database")
        return db.load_remote_data("rooms.json", eval_output=True, branch="database")[roomname]
    
    rooms[roomname].append(data)
    db.push_remote_data(rooms, "rooms.json", branch="database")
    return db.load_remote_data("rooms.json", eval_output=True, branch="database")[roomname]


def get_avatar(_ip):
	con = db.load_remote_data("avatars.json", eval_output=True, branch="database")
	try:
		return con['ip_avatars'][_ip]
	except KeyError:
		con['ip_avatars'].update({_ip : requests.get(f"https://loremflickr.com/json/320/320/{WOTD}").json()['file']})
		db.push_remote_data(con, "avatars.json", branch="database")
		return con['ip_avatars'][_ip] # returns new complete json


def set_avatar(_ip,av):
    con = db.load_remote_data("avatars.json", eval_output=True, branch="database")
    con['ip_avatars'].update({_ip : av})
    db.push_remote_data(con, "avatars.json", branch="database")
    return {_ip : av}




