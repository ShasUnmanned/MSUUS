import sys
from LatLon import *

def main(argv):
	print(argv)
	print(argv[0])
	output_str = string2latlon(argv[0], argv[1], 'd% %m% %S% H')
	print(output_str.to_string('d%_%M'))

if __name__ == "__main__":
	main(sys.argv[1:])
