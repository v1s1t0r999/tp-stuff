from . import database
from datetime import datetime
import requests as r
from flask import Flask, request, render_template, redirect



app = Flask(__name__)



@app.route("/")
def index():
	return redirect("/room")


@app.errorhandler(404)
def notfound(e):
	try:
		return render_template(request.path)
	except:
		return str(e)



@app.route("/room/<name>", methods=["GET","POST"])
def room(name):
	if request.method=="POST":
		user = str(request.remote_addr)
		timestamp = datetime.now().strftime("%H:%M:%S")
		content = request.form['content']
		if content.lower() in ["!!avatar","!!av"]:
			av_url = content.lower().split(" ")
			if len(av_url)==1:
				return redirect(f"/room/{name}")
			try:
				img = requests.get(av_url[1])
				db.set_avatar(request.remote_addr,img)
				return  redirect(f"/room/{name}")
			except requests.exceptions.ConnectionError:
				return redirect(f"/room/{name}")
		if content=="":
			return redirect(f"/room/{name}")
		database.add(name,{'from':user,'content':content,'timestamp':timestamp,'avatar':database.get_avatar(user)})
		return redirect(f"/room/{name}")
	name=str(name)
	messages = database.read(name) #list like: [{"from":"user","msg":"this this"},{"from":"another","msg":"ok ok"}]
	return render_template("chatarea.html",messages=messages,roomname=name,_ip=request.remote_addr)



@app.route("/room", methods=["GET","POST"])
def room_base():
	if request.method=="POST":
		roomname = request.form['roomname']
		return redirect(f"/room/{roomname}")
	return render_template("room.html", _ip=request.remote_addr, active_rooms=list(database.read()))





def run(debug=False):
	app.run("0.0.0.0", debug=debug)

	
	
if __name__=="__main__":
	run(debug=True)
