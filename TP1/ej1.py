#Le pongo .py para tener el syntax highlight de python, en realidad hay que correrlo con scapy

def quienTiene(ip):
	#Creamos un nuevo paquete ARP y le seteamos la dirección ip cuya mac quiero averiguar
	arp = ARP()
	arp.setfieldval('pdst', ip)
	#Lo mandamos y esperamos respuesta
	rec = sr(arp, timeout = 1)
	#Lo mostramos lindo
	rec[0].show()
	#Armamos una lista de mappings 'ip': dir ip, 'mac': dir mac (como para hacer algo más)
	lst = []
	if len(rec) > 0:
		for pkg in rec[0]:
			lst.append({'ip': pkg[0].pdst, 'mac' : pkg[1].hwsrc })
	return lst

def buscar(ipBase, step = 1):
	"""ipBase es de la forma XX.XX.XX., step es cada cuántas IPs queremos preguntar"""
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
	