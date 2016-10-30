import interop
import sys
import re
import Tkinter
from Tkinter import *


def main():
	telemetry_open = False
	

	def connect(url, username, password):
		#set up the connection to the interop server at the specified
		#url with the specified username/password
		client = interop.Client(url=url,
		                        username=username,
		                        password=password)
	
		#create an object with telemetry info (we will be getting the
		#telemetry info from the autopilot so this code would have to
		#run on the GCS machine as a MissionPlanner script)
		telemetry = interop.Telemetry(latitude=38.145215,
		                              longitude=-76.427942,
		                              altitude_msl=50,
		                              uas_heading=90)
		#send that info to the interop server
		client.post_telemetry(telemetry)
		
		#create a target object. we will be building this object using 
		#the output of our image classification program, from values
		#stored in our database.
		target = interop.Target(type='standard',
		                        latitude=38.145215,
		                        longitude=-76.427942,
		                        orientation='n',
		                        shape='square',
		                        background_color='green',
		                        alphanumeric='A',
		                        alphanumeric_color='white')
		#send the target info to the interop server
		target = client.post_target(target)
		print(client.get_targets())
		print(client.get_obstacles())

	def telemetry_tab():
		#if (telemetry_open == False):
			data_rate_label = Label( window, text="Telemetry Data Rate:" )
			data_rate_field = Entry( window )
		#	telemetry_open = True
		#else:
		#	telemetry_open = False

	window = Tkinter.Tk()
	window.title("MSUUS")
	window.geometry("640x640")

        url = StringVar( window )
        url.set('http://127.0.0.1:8000')
        username = StringVar( window )
        username.set('testuser')
        password = StringVar( window )
        password.set('testpass')
	
	url_label = Label( window, text="Server URL")
	url_label.grid(row=0,column=0)
	url_textbox = Entry( window, textvariable=url )
	url_textbox.grid(row=0,column=1)

	username_label = Label( window, text="Username:")
	username_label.grid(row=1,column=0)
	username_textbox = Entry( window, textvariable=username )
	username_textbox.grid(row=1,column=1)

	password_label = Label( window, text="Password:")
	password_label.grid(row=2,column=0)
	password_textbox = Entry( window, textvariable=password )
	password_textbox.grid(row=2,column=1)

	connect_button = Button( window, text="Connect", command = connect(url.get(),username.get(),password.get()) )
	connect_button.grid(row=3,column=1)

	output_label = Label( window, text="Output" )
	output_label.grid(row=5,column=0)
	output_textbox = Text( window, width=20 )
	output_textbox.grid(row=5,column=1)

	telemetry_tab_button = Button( window, text="Telemetry", command = telemetry_tab() )
	
	#url_label.pack()
	#url_textbox.pack()
	#username_label.pack()
	#username_textbox.pack()
	#password_label.pack()
	#password_textbox.pack()
#	connect_button.pack()
#	output_label.pack()
#	output_textbox.pack()
#	telemetry_tab_button.pack()
	
	window.mainloop()


if __name__ == "__main__":
	main()
