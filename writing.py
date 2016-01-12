#!/usr/bin/env python3

f = open('scores.txt','w')

while True:
	participant = input("Participant name: ")
	
	if participant == 'quit':
		print("Quitting")
		break
		
	score = input("Score for participant '" + participant +"':")
	f.write(participant + ',' + score + '\n')
	
print("Done")
f.close()
