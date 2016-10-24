import interop

#set up the connection to the interop server at the specified
#url with the specified username/password
client = interop.Client(url='http://127.0.0.1:8000',
                        username='testuser',
                        password='testpass')

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
