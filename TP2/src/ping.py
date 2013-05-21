#!/usr/bin/python

from scapy.all import *
from optparse import OptionParser
import time

def ping(host, cant=4, p_ttl=64):
	#creamos un paquete icmp sobre un paquete ip
	icmp = IP(dst=host, ttl=p_ttl) / ICMP() / 'Pingeando host'

	printf('Pingeando %r usando TTL=%r', host, p_ttl)

	try:
		for i in range(1, cant+1):
			rep = None
			secs = time.time()
			rep = sr1(icmp, verbose=0, timeout=3)
			secs = round(time.time() - secs, 4)

			if rep == None:
				print 'Ping no respondido'
			else:
			
				host_rep = rep[0].src

				printf('Reply obtenido de %r en %r segundos', host_rep, secs)

	except:

		return -1

	return 0


def definirParamertos(parser):
	parser.add_option("-c", "--cant", default=4, dest='cant' , help='cantidad de pings a enviar (default = 4)')
	parser.add_option("-t", "--time-to-live", default=64, dest='ttl', help='tiempo de vida de los paquetes ICMP (default = 64)')
	parser.add_option("-o", "--host", default='localhost', dest='host', help='ip destino del ping (default = localhost)')
	
	(params, args)=parser.parse_args()

	return params


def printf(format, *args):
    sys.stdout.write(format % args)
    sys.stdout.write('\n')
	
if __name__ == '__main__':

	usage = "usage: sudo %prog [options] -o <host>"

	#parseamos los parametros
	parser=OptionParser(usage=usage)
	params = definirParamertos(parser)
	
	if os.geteuid() or not params.host:
		parser.print_help()
		exit()

	exit_code = ping(params.host, params.cant, params.ttl)

	if exit_code == -1:
		print 'Hubo un problema al realizar el ping'

	exit(exit_code)

