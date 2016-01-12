#!/usr/bin/env python3

import time
import os

class Timer:
	def __init__(self):
		self.time = time.localtime()
		
	def __str__(self):
		return time.strftime('%H:%M:%S',self.time)
		
guesses = 0
tr = Timer()

while guesses < 12:
	
	while !string:
		string = input("Guess a letter: ")
		while 1:
			print("\r" + tr,end='')
			if string:
				break
				
