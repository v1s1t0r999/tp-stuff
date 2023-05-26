from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
	return "index"

@app.errorhandler(404)
def notfound(e):
	return f"{str(e)}<hr><hr>{dir(e)}"

def run(debug=False):
	app.run("0.0.0.0", debug=debug)

	
	
if __name__=="__main__":
	run()
