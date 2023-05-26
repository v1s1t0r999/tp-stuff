from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
	return "index"

def run(debug=False):
	app.run("0.0.0.0", debug=debug)

if __name__=="__main__":
	run()
