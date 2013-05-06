#!/usr/bin/python

import sys
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def quienTiene(ip):

	try:
		# redireccionamos stdout a /dev/null para no ver la salida del scapy
		f = open(os.devnull, 'w')
		stdout = sys.stdout
		sys.stdout = f
		
		# Creamos un nuevo paquete ARP y le seteamos la direccion ip cuya mac quiero averiguar
		arp = ARP()
		arp.setfieldval('pdst', ip)
		
		#Lo mandamos y esperamos respuesta
		rec = sr(arp, timeout = 3)
		
		#Lo mostramos lindo
		rec[0].show()
		
		#Armamos lista de macs recibidas para devolver
		lst = []
		if len(rec) > 0:
			for pkg in rec[0]:
				lst.append(pkg[1].hwsrc)

	except:
		return -1

	finally:
		# restauramos stdout
		sys.stdout = stdout

	return lst

def buscar(ipBase, step = 1):
	"""ipBase es de la forma XX.XX.XX., step es cada cuantas IPs queremos preguntar"""
	maps = {}
	for i in range(1, 255 / step):
		ipArmada = ipBase + str(step * i)
		ips = quienTiene(ipArmada)
		
		if ips == -1:
			print 'Error al buscar direccion MAC'
			exit()

		if len(ips) == 0:
			maps[ipArmada] = []
		else:
			for i in ips:
				if i['ip'] in maps:
					maps[i['ip']].append(i['mac'])
				else:
					maps[i['ip']] = [i['mac']]
	return maps


if __name__ == '__main__':

	if os.geteuid():
		print "Vuelve cuando seas root (correr con sudo :) )"
		exit()

	if len(sys.argv) < 2:
		print "Usar: ./ej1 <numero ip>"
		exit()

	ip = sys.argv[1]

	print "IP destino:", ip

	ips = quienTiene(ip)
	if ips == -1:
		print 'Error al buscar direccion MAC'
		exit()

	macs = quienTiene(ip)
	print

	if len(macs) == 0:
		print ip, 'no es una ip valida o no puede ser alcanzada'
	elif len(macs) == 1:
		print 'Mac:', macs[0]
	else:
		print 'Macs:',
		for mac in macs:
			print mac,

	exit()
