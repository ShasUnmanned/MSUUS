import requests

class UAV:

	def __init__(self, url, username, password):
		self.url = url
		self.username = username
		self.password = password
		
	def get(endpoint):
		r = requests.get(self.url + endpoint, auth=(self.username, self.password))
		return r.json()
		
	def bottle_drop():
		return self.get('/bottle_release')
		
	def take_picture():
		return self.get('/take_picture')
		
	def get_gps():
		return self.get('/get_gps')
		
	def start_video():
		return self.get('/start_video_stream')
		
	def restart():
		return self.get('/restart_listener')

