from . import database
from flask import Flask, request, render_template



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



@app.route("/room/<name>")
def room(name):
	name=str(name)
	messages = database.read(name) #list like: [{"from":"user","msg":"this this"},{"from":"another","msg":"ok ok"}]
	return render_template("chatarea.html",messages=messages)



def run(debug=False):
	app.run("0.0.0.0", debug=debug)

	
	
if __name__=="__main__":
	run(debug=True)
