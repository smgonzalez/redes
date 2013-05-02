#!./bin/python
#Le pongo .py para tener el syntax highlight de python, en realidad hay que correrlo con scapy

from sys import argv
from scapy.all import *

def quienTiene(ip):
	# Creamos un nuevo paquete ARP y le seteamos la direccion ip cuya mac quiero averiguar
	arp = ARP()
	arp.setfieldval('pdst', ip)
	#Lo mandamos y esperamos respuesta
	rec = sr(arp, timeout = 1)
	#Lo mostramos lindo
	rec[0].show()
	#Armamos una lista de mappings 'ip': dir ip, 'mac': dir mac (como para hacer algo mas)
	lst = []
	if len(rec) > 0:
		for pkg in rec[0]:
			lst.append({'ip': pkg[0].pdst, 'mac' : pkg[1].hwsrc })
	return lst

def buscar(ipBase, step = 1):
	"""ipBase es de la forma XX.XX.XX., step es cada cuantas IPs queremos preguntar"""
	maps = {}
	for i in range(1, 255 / step):
		ipArmada = ipBase + str(step * i)
		ips = quienTiene(ipArmada)
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
	if len(argv) < 2:
		print "Usar: ./ej1 <numero ip>"
		exit()

	ip = argv[1]

	print "IP destino:", ip
	print quienTiene(ip)
