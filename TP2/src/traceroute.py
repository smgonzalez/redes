#!/usr/bin/python

from scapy.all import *
from optparse import OptionParser

def traceroute(host, ttl_max=64):
	route=[]
	pkg=IP(dst=host) / ICMP() / 'Pingeando host'

	try:
		for i in range(1, ttl_max+1):
			pkg.ttl = i
			rep = sr1(pkg, verbose=0, timeout=3)

			if rep == None:
				ip = '-'
			else:
				ip = rep[0].src
			
			route.append(ip)

			if ip = host:
				break

	except:
		return -1

	i=1
	print 'Ruta:'
	for ip in route:
		print i, ')', ip
		i+=1
	
	return 0


def definirParamertos(parser):
	parser.add_option("-t", "--time-to-live-max", default=64, dest='ttl', help='tiempo de vida maximo de los paquetes ICMP (default = 64)')
	parser.add_option("-o", "--host", default='localhost', dest='host', help='ip destino del traceroot (default = localhost)')
	
	(params, args)=parser.parse_args()

	return params


if __name__ == '__main__':

	usage = "usage: sudo %prog [options] -o <host>"

	#seteamos parser de los parametros
	parser=OptionParser(usage=usage)
	params = definirParamertos(parser)
	
	# si no usaste sudo o no pasate el host, mostra help
	if os.geteuid() or not params.host:
		parser.print_help()
		exit()

	exit_code = traceroute(params.host, params.ttl)

	if exit_code == -1:
		print 'Hubo un problema al generar la ruta'
	
	exit(exit_code)
