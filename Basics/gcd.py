#!/usr/bin/env python3
# gcd.py: Calculates the greatest common divisor of the numbers a and b

def gcd(a,b):
	if not b == 0:
		return gcd(b,a % b)
	else:
		return a

if __name__ == '__main__':		
	import sys
	x = int(sys.argv[1])
	y = int(sys.argv[2])
	print(gcd(x,y))
