#coding: utf-8

import datetime
import collections
import math
import parser

def entropia(counter):
	#counter[s] = cantidad de apariciones del símbolo s (positivas)
	#counter.values() = [cantidad de apariciones de s for s in símbolos]
	#counter.keys() = [símbolos]
	total = float(sum(counter.values())) #cantidad de paquetes capturados
	#fórmula individual de la entropía, medida en base 2 (bits)
	ponderacion = lambda s: counter[s]/total * (math.log(total/counter[s], 2))
	#sumatoria ponderada para cada símbolo
	return sum(map(ponderacion, counter.iterkeys()))

def contarSimbolos(dump, startTime = None, endTime = None):
	f = open(dump, 'r')
	startEndFilter = lambda l: parser.filtrarPorTiempo(l, startTime, endTime)
	#Leemos sólo las líneas que pasan el filtro startEndFilter (ver parser.py)
	l = parser.readFilteredLine(f, startEndFilter)
	#Cantidad: dicc((ipSrc, ipDst) => cantidadDeApariciones)
	cantidad = collections.Counter()
	while l:
		l = l.split()
		#Normalizamos el par (ipSrc, ipDst) como el string que resulta de concatenarlos para poder usarlos de índice: norm((ipSrc, ipDst)) = ipSrc-ipDst
		#Es claro que resulta (ipSrc, ipDst) = (iprc', ipDst') <=> norm(ipSrc, ipDst) = norm(ipSrc', ipDst')
		cantidad[l[1]+'-'+l[2]] += 1 #si la clave k no está definida, cantidad[k] = 0
		l = parser.readFilteredLine(f, startEndFilter)
	return cantidad

def contarHosts(dump):
	#perdón por el copy-paste
	f = open(dump, 'r')
	filtrarWhos = lambda l: l and l.split()[0] == '1'
	#Leemos sólo los who-has
	l = parser.readFilteredLine(f, filtrarWhos)
	#Cantidad: dicc(ipDst => cantidadDeApariciones)
	cantidad = collections.Counter()
	while l:
		l = l.split()
		cantidad[l[1]] += 1 #si la clave k no está definida, cantidad[k] = 0
		l = parser.readFilteredLine(f, filtrarWhos)
	return cantidad

def calcularTodo(dump, startTime = None, endTime = None):
	if type(startTime) == str:
		startTime = parser.parseStrTime(startTime)
	if type(endTime) == str:
		endTime = parser.parseStrTime(endTime)
	return entropia(contarSimbolos(dump, startTime, endTime))

def calcularInfoPorHost(dump):
	todosLosHosts = contarHosts(dump)
	todosLosPedidos = sum(todosLosHosts.itervalues())
	infoPorHost = {}
	for d in todosLosHosts.iteritems():
		#para cada host obtenido, calculamos la cantidad de información que aporta al aparecer.	
		infoPorHost[d[0]] = -math.log(float(d[1])/todosLosPedidos)
	return infoPorHost
