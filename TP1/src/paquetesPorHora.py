#!/usr/bin/python

from parser import parseStrTime
from sys import argv

fileIn = open(argv[1], 'r')
fileOut = open(argv[2], 'w')

hours_dict = {}
for l in fileIn:
	date = l.split()[5] 

	hour = parseStrTime(date).tm_hour
	if hour not in hours_dict:
		hours_dict[hour] = 0
	
	hours_dict[hour]+=1

for key, value in hours_dict.items():
	fileOut.write(str(key)+' '+str(value)+'\n')
	print str(key)+' '+str(value)+'\n'

fileIn.close()
fileOut.close()
