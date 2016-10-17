from flask import Flask
from subprocess import call

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World!'

# run a command passed by POST method as a shell command on the pi
# example would  be like http://serverurl:5000/run_command?command=something&options=somethingelse
# might not work and might need to be passed as a json object
@app.route('/run_command', methods=['POST'])
def run_command(command, options):
    subprocess.call([request.form['command'], request.form['options']])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
