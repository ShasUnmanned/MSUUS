from flask import Flask
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/run_command')
def run_command(command, options):
    subprocess.call([command, options])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
