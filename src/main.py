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

def run(debug=False):
	app.run("0.0.0.0", debug=debug)

	
	
if __name__=="__main__":
	run()
