from flask import Flask, jsonify
from subprocess import call
import sys
import io
import os
import shutil
from subprocess import Popen, PIPE
from string import Template
from struct import Struct
from threading import Thread
from time import sleep, time

import picamera
import time
import base64


app = Flask(__name__)

camera = picamera.PiCamera()
camera.resolution = (3280, 2464)
cap_count = 0
Acap_count = 0
autopic = False
 
@app.route('/')
def hello_world():
	return 'MSUUS PI PAYLOAD'

# run a command (contained in a json object) passed by POST method as a shell command on the pi
@app.route('/run_command', methods=['GET', 'POST'])
def run_command():
	request_data = request.get_json()
	subprocess.call([request_data['command'], request_data['options']])
	return Flask.jsonify( {
		"status": "ok",
		})

@app.route('/get_gps', methods=['GET'])
def get_gps():
	#######################################
	# need to actually get the gps somehow#
	#######################################
	return jsonify( {
		"latitude": latitude,
		"longitude": longitude,
		})

@app.route('/take_picture', methods=['GET'])
def take_picture():
	global cap_count, camera
	cap_count += 1
	sleep(2)
	filename = 'test_capture_'+str(cap_count-1)+'.jpg'
	camera.capture(filename)

	#return flask.send_file(filename, mimetype='image/jpg')
	
	with open(filename, "rb") as image_file:
    		encoded_image = base64.b64encode(image_file.read())

	return jsonify( {
		"id": (cap_count-1),
		"image": encoded_image,
		})

@app.route('/start_autopicture', methods=['POST'])
def start_autopicture():
	global autopic
	autopic = True
	return Flask.jsonify( {
		"status": "ok",
		})

@app.route('/stop_autopicture', methods=['POST'])
def start_autopicture():
	global autopic
	autopic = False
	return Flask.jsonify( {
		"status": "ok",
		})


@app.route('/bottle_release')
def bottle_release():
	######################################
	#do_release():                       #
	######################################
	return jsonify( {
		"bottle_release":"released",
		"release_time":time.time(),
		})

@app.route('/restart_listener')
def restart_listener():
	print('pi listener is restarting')
	'''
	executable = sys.executable
	args = sys.argv[:]
	args.insert(0, sys.executable)

	time.sleep(1)
	os.execvp(executable, args)
	'''
	subprocess.call(['python pi_listener.py'])
	time.sleep(1)
	exit()
	print('did it make it here?')

@app.route('/stop_listener')
def stop_listener():
	print('pi listener is stopping')
	exit()


def take_autopicture():
	global Acap_count, camera
	Acap_count += 1
	sleep(2)
	filename = 'autopic/test_capture_'+str(cap_count-1)+'.jpg'
	camera.capture(filename)
	


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)


@app.route('/start_video_stream', methods=['GET', 'POST'])
def start_video_stream():
	return 0

