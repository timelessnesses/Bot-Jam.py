import flask
import threading
app = flask.Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

def run():
    app.run(host='0.0.0.0', port=80)

def alive():
    threading.Thread(target=run).start()