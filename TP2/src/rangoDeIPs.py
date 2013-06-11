import sys
import re

# ipSrc = sys.argv[1]
# maskSrc = int(sys.argv[2])
# ipDst = sys.argv[3]
# maskDst = int(sys.argv[4])

masked = lambda ip, mask: ip[:-mask] if mask else ip

def buscarEnLineas(ipSrc, maskSrc, ipDst, maskDst, fileLines):
	"""devuelve el hop donde termina el enlace buscado, que empieza en la red ipSrc/maskSrc y termina en ipDst/maskDst, donde mask es en caracteres"""
	ipsAnteriores = {}
	ipsActuales = {}
	for actual in fileLines:
		matches = re.search(
			# nro de hop        ((nombre) IP del server        RTT) o un *   
			'\s*([0-9]{,2})\s+(?:(?:.+?\s*\(([0-9.]+)\))\s+((?:\s*[0-9.]+\s+ms)+)\s+|\*)$'
			, actual
		) #pueden ir a http://www.regexper.com/ y ver que significa
		if matches.group(1): #es un nuevo hop
			hop = matches.group(1)
			ipsAnteriores = ipsActuales
			ipsActuales = {}
		ip = matches.group(2)
		if ip:	#me respondieron
			if masked(ip, maskDst) == masked(ipDst, maskDst) and ipsAnteriores.__contains__(masked(ipSrc, maskSrc)):
				parsearTiempos = lambda string: map(float, re.findall('(?:\s*([0-9.]+)+\s+ms)', string))
				promedio = lambda l: sum(l)/len(l)
				tiempoAnterior = promedio(parsearTiempos(ipsAnteriores[masked(ipSrc, maskSrc)]))
				tiempoActual = promedio(parsearTiempos(matches.group(3)))
				rtt = tiempoActual - tiempoAnterior
				return hop, rtt
			else:
				if ipsActuales.__contains__(masked(ip, maskDst)):
					ipsActuales[masked(ip, maskSrc)] += ' ' + matches.group(3)	#te quiero python
				else:
					ipsActuales[masked(ip, maskSrc)] = matches.group(3)
	return -1, 0

f = open(sys.argv[5], 'r')
hop, rtt = buscarEnLineas(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), f)
f.close()
if (hop > 0):
	print int(hop) - 4 if hop >= 4 else 0, int(hop) + 3, rtt
	exit(0)
else:
	exit(-1)





#Eth2.sb01.eur.prosodie.net (195.46.192.213)  269.273 ms  263.396 ms  262.105 ms Eth2.sb02.eur.prosodie.net (195.46.192.125)  276.405 ms  277.686 ms Eth2.sb01.eur.prosodie.net (195.46.192.213)  264.833 ms Eth2.sb02.eur.prosodie.net (195.46.192.125)  277.959 ms Eth2.sb01.eur.prosodie.net (195.46.192.213)  265.962 ms  269.228 ms Eth2.sb02.eur.prosodie.net (195.46.192.125)  270.891 ms
