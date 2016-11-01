import interop
import sys
import re
import Tkinter
from Tkinter import *


def main():
	telemetry_open = False
	client = interop.Client(url='http://127.0.0.1:8000', username='testuser', password='testpass')
	
	def upload_telemetry(client, out):
                telemetry = interop.Telemetry(latitude=38.145215,
			longitude=-76.427942,
			altitude_msl=50,
			uas_heading=90)
                #send that info to the interop server
                client.post_telemetry(telemetry)
		out.insert(END,"Telemetry posted")

	def upload_target(client, out):
		try:
                        #create a target object. we will be building this objec$
                        #the output of our image classification program, from v$
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
                        out.insert(END, client.get_obstacles())
		except:
			out.insert(END, 'something went wrong when uploading target')


	def connect(url, username, password, out):
		try:
			#set up the connection to the interop server at the specified
			#url with the specified username/password
			client = interop.Client(url=url,
			                        username=username,
			                        password=password)
		except:
			out.insert(END, "something when wrong when trying to connect")	

	def telemetry_tab():
		#if (telemetry_open == False):
			data_rate_label = Label( window, text="Telemetry Data Rate:" )
			data_rate_field = Entry( window )
		#	telemetry_open = True
		#else:
		#	telemetry_open = False

	window = Tkinter.Tk()
	window.title("MSUUS")
	window.geometry("660x500")

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

	output_label = Label( window, text="Output" )
	output_label.grid(row=5,column=0)
	output_textbox = Text( window )
	output_textbox.grid(row=5,column=1)

        connect_button = Button( window, text="Connect", command = lambda: connect(url.get(),username.get(),password.get(),output_textbox) )
        connect_button.grid(row=3,column=0)


	telemetry_tab_button = Button( window, text="Telemetry", command = telemetry_tab() )
	#telemetry_tab_button.grid(row=3,column=2)


	target_upload_button = Button( window, text="Upload Target", command = lambda: upload_target(client, output_textbox) )
	target_upload_button.grid(row=3,column=1)


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

	window.after(500, lambda: upload_telemetry(client,output_textbox))	
	window.mainloop()


if __name__ == "__main__":
	main()
