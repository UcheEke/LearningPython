#!/usr/bin/env python3

"This program simply squares the input unless it recieves an EOF"

def interact():
	while True:
		try:
			num = input("Enter an integer: ")
		except EOFError:
			break
		else:
			num = int(num)
			print('The number {} squared is {}'.format(num,num**2))
	print('Bye')
	
if __name__ == '__main__':
	interact()
	
