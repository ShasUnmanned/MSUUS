import sys
from LatLon import *

def main(argv):
	output_str = string2latlon(argv[0], argv[1], 'd% %m% %S% H')
	print(output_str)

if __name__ == "__main__":
	main(sys.argv[1:])
