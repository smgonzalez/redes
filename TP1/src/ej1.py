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
		
		#Lo mostramos
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
	#por si recibimos mas de una respuesta
	elif len(macs) == 1:
		print 'MAC:', macs[0]
	else:
		print 'MACs:',
		for mac in macs:
			print mac,

	exit()
