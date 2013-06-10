#!/usr/bin/python

from scapy.all import *
from optparse import OptionParser
import time
import datetime

def traceroute(host, ttl_max=64, pkgs_per_ttl=1):
	
	ttl = int(ttl_max)
	num_pkgs = int(pkgs_per_ttl)
	
	# num_pkgs: Cantidad de paquetes que se envian por cada ttl
	#route=[]
	pkg=IP(dst=host) / ICMP() / 'Pingeando host'
	
	print datetime.datetime.now()
	
	for i in range(1, ttl+1):
		
		#print 'pingeando i:', i
		pkg.ttl = i
		strRes = 'Hop ' + str(i) + '\t'
		
		ready = 0
		contin = 0
		ip_ok = 0
		
		rtts = []
		
		for p in range(1, num_pkgs+1):
			
			ans = None
			
			t0 = time.time()
			ans = sr1(pkg, verbose=0, timeout=3)
			rtt = time.time() - t0
			
			if ans == None:
				ip = '-'
			else:
				ip = ans[0].src
				ip_ok = 1
				
				# Solo entran al promedio los rtts de respuestas correctas
				rtts.append(rtt)
				
				if ans[1].type == 0:		# Recibi paquete ICMP del tipo echo-reply
					ready = 1
					break
				
			strRes += ip + '\t' + str(round(rtt,4)*100) + 'ms\t'

			if ip == host:
				ready = 1
				break

		if ready:
			break
		elif contin:
			continue
			
		#route.append(ip)
		# Saco RTT promedio
		if ip_ok:
			avgRTT = reduce(lambda x,y:float(x)+float(y), rtts)/len(rtts)
			strRes += 'RTT Promedio: ' + str(round(avgRTT, 4)*100) + 'ms (sobre ' + str(len(rtts)) + ' paquetes)'
			print strRes

#	i=1
#	print 'Ruta:'
#	for ip in route:
#		print i, ')', ip
#		i+=1
	
	return 0


def definirParamertos(parser):
	parser.add_option("-t", "--time-to-live-max", default=64, dest='ttl', help='Tiempo de vida maximo de los paquetes ICMP (default = 64)')
	parser.add_option("-o", "--host", default='localhost', dest='host', help='IP destino del traceroot (default = localhost)')
	parser.add_option("-p", "--packages-per-ttl", default=1, dest='pkgs_per_ttl', help='Cantidad de paquetes a enviar por cada ttl (default = 1)')
	
	(params, args)=parser.parse_args()

	return params


if __name__ == '__main__':

	usage = "usage: sudo ./traceroute.py [options] -o <host>"

	#seteamos parser de los parametros
	parser=OptionParser(usage=usage)
	params = definirParamertos(parser)
	
	# si no usaste sudo o no pasate el host, mostra help
	if os.geteuid() or not params.host:
		parser.print_help()
		exit()

	exit_code = traceroute(params.host, params.ttl, params.pkgs_per_ttl)

	if exit_code == -1:
		print 'Hubo un problema al generar la ruta'
	
	exit(exit_code)
