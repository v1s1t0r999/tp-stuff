#do2
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
		if content.lower().startswith("!!av"):
			av_url = content.lower().split(" ")
			if len(av_url)==1:
				return redirect(f"/room/{name}")
			try:
				img = r.get(av_url[1])
				database.set_avatar(request.remote_addr,av_url[1])
				return  redirect(f"/room/{name}")
			except:
				return redirect(f"/room/{name}")
		if content.lower().startswith("!!rm"):
			rname = content.lower().split(" ")[1]
			cnt = f"<a href='/room/{rname}'> <b>{rname}</b> </a>"
			 database.add(name,{'from':user,'content':cnt,'timestamp':timestamp,'avatar':database.get_avatar(user)})
			 return  redirect(f"/room/{name}")
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
		roomname = request.form['roomname'].replace("%20","-").replace(" ","-")
		return redirect(f"/room/{roomname}")
	return render_template("room.html", _ip=request.remote_addr, active_rooms=list(database.read()))





def run(debug=False):
	app.run("0.0.0.0", debug=debug)

	
	
if __name__=="__main__":
	run(debug=True)
