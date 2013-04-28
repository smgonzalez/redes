#Le pongo .py para tener el syntax highlight de python, en realidad hay que correrlo con scapy

def quienTiene(ip):
	arp = ARP()
	arp.setfieldval('pdst', ip)
	rec = sr(arp, timeout = 1)
	rec[0].show()
	lst = []
	for pkg in rec[0]:
		lst.append({'ip': pkg[0].pdst, 'mac' : pkg[1].hwsrc })
	return lst


