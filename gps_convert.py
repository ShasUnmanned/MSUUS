import sys
import re

def to_decimal(in_str):
	(d,m,s,h) = re.split('\s',in_str, maxsplit=4)
	if (re.search('[swSW]', in_str)):
		sign = -1
	else:
		sign = 1
	return sign * (int(d) + float(m) / 60 + float(s) / 3600)

def main(argv):
	output_str = str(to_decimal(argv[0])) + ' ' + str(to_decimal(argv[1]))
	print(output_str)

if __name__ == "__main__":
	main(sys.argv[1:])
