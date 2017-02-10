import sys, math

def get_location(x, y, fov, altitude, gps):
	""" Takes an x,y coordinate of a target in an image, and uses the 
	current altitude, gps coordinates, and camera field of view to 
	calculate the gps position of the target. """

	dx = x*(fov[0]*altitude) # x distance from image center in meters
	dy = y*(fov[1]*altitude) # y distance from image center in meters
	
	### still need to rotate dx,dy by the current drone orientation ###	
	
	lat = gps[0] + (180/pi)*(dy/6378137)
	lon = gps[1] + (180/pi)*(dx/6378137)/cos(gps[1])

	return [lat, lon]

	
