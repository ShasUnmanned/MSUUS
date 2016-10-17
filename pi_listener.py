from flask import Flask
from subprocess import call

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World!'

# run a command (contained in a json object) passed by POST method as a shell command on the pi
@app.route('/run_command', methods=['GET', 'POST'])
def run_command():
	request_data = request.get_json()
	subprocess.call([request_data['command'], request_data['options']])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
