#!/usr/bin/env python3

f = open('scores.txt','r')

participants = {}

for line in f:
	line = line.strip().split(',')
	participants[line[0]] = line[1]
	
print(participants)	
f.close()
