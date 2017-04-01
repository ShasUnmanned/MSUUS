### r
Script.ChangeMode("Guided")                     # changes mode to "Guided"
print 'Guided Mode'
item = MissionPlanner.Utilities.Locationwp() # creating waypoint
lat = 39.343674                                           # Latitude value
lng = -86.029741                                         # Longitude value
alt = 45.720000                                           # altitude value
MissionPlanner.Utilities.Locationwp.lat.SetValue(item,lat)     # sets latitude
MissionPlanner.Utilities.Locationwp.lng.SetValue(item,lng)   # sets longitude
MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt)     # sets altitude
print 'WP 1 set'
MAV.setGuidedModeWP(item)                                    # tells UAV "go to" the set lat/long @ alt
print 'Going to WP 1'
time.sleep(10)                                                            # wait 10 seconds
print 'Ready for next WP'



import sys
import clr
import MissionPlanner
import MySQLdb

print 'Starting Mission Controller...\n"
clr.AddReference("MissionPlanner.Utilities")
missionData = False # is mission data available? flag
print 'Switching to Guided mode.\n'
Script.ChangeMode("Guided")                      # changes mode to "Guided"

### DB Connection ###

print 'Connecting to database...\n'
try:
	db = MySQLdb.connect(host = "localhost", user="root", passwd = "password", db ="MSUUS")
	print 'Connected.\n'
except:
	print 'Error connecting to database.\n'
	
### Search For Missions Loop ###

while not missionData:
	cur = db.cursor() #allows execution of all SQL queries
	cur.execute("SELECT * FROM targets")
	if cur.fetchAll():
		missionData = True

### Download Mission Data & Set ###


### Reroute Around Obstacles ###
