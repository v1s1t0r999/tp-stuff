from . import database
from datetime import datetime
from flask import Flask, request, render_template, redirect



app = Flask(__name__)



@app.route("/")
def index():
	return "index"


@app.errorhandler(404)
def notfound(e):
	try:
		return render_template(request.path)
	except:
		return str(e)



@app.route("/room/<name>", methods=["GET","POST"])
def room(name):
	if request.method=="POST":
		print("POST TRIGGERED")
		user = str(request.remote_addr)
		timestamp = datetime.now().strftime("%H:%M:%S")
		content = request.form['contents']
		if content=="":
			print("|||||| no content |||")
			return redirect(f"/room/{name}")
		database.add(name,{'from':user,'content':content,'timestamp':timestamp})
		print("hereeeeeeeeeee")
		return redirect(f"/room/{name}")
	print("GET TRIGGERED")
	name=str(name)
	messages = database.read(name) #list like: [{"from":"user","msg":"this this"},{"from":"another","msg":"ok ok"}]
	return render_template("chatarea.html",messages=messages,roomname=name)



def run(debug=False):
	app.run("0.0.0.0", debug=debug)

	
	
if __name__=="__main__":
	run(debug=True)
