#!/usr/bin/python
# script echo en 2 minutos para filtrar ips con cantidad baja de consultas xD, lo subo por si lo tengo q reusar y no estoy en mi casa..

from sys import argv

fileIn = open(argv[1],'r')
fileOut = open(argv[2], 'w')

for l in fileIn:
	cant = l.split()[1]
	
	if int(cant) > int(argv[3]):
		fileOut.write(l)

fileIn.close()
fileOut.close()
