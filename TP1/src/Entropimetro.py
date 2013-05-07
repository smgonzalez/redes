#!/usr/bin/python
#coding: utf-8

import sys

import sys
import datetime
import os
import re
import collections
import math
import parser

params_readTime  = 'readtime' #con qué formato interpreto el timestamp
params_timePlace = 'timeplace' #en qué índice de split(línea de entrada) está el timestamp
params_history = 'history' #en minutos, cuánta historia consideramos
params_dataPlace = 'dataplace' #qué índices de split(línea de entrada) consideramos como información
params_live = 'live'

params = {params_readTime : None,
	params_timePlace : None,
	params_history: None,
	params_dataPlace : None,
}

# def parseParams(args):
# 	#--paramA = valorA --paramB = valorB ...
# 	argString = reduce(lambda a, b: a+' '+b, args)
# 	paramDict = {}
# 	for paramKey in params.iterkeys():
# 		regex = re.compile('(?:.+?|^)--'+paramKey+'\s*=\s*(?P<'+paramKey+'>.+?)(?:\s|$)') #odio las expresiones regulares profundamente
# 		valor = regex.match(argString)
# 		if (valor):
# 			paramDict.update(valor.groupdict())
# 	for k, v in paramDict.iteritems():
# 		if k == params_readTime or k == params_history:
# 			paramDict[k] = int(v)
# 		elif k == params_dataPlace:
# 			paramDict[k] = map(int, v.split(','))
# 	return paramDict

def entropia(counter):
	#counter[s] = cantidad de apariciones del símbolo s (positivas)
	#counter.values() = [cantidad de apariciones de s for s in simbolos]
	#counter.keys() = [simbolos]
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

def calcularTodo(dump, startTime = None, endTime = None):
	if type(startTime) == str:
		startTime = parser.parseStrTime(startTime)
	if type(endTime) == str:
		endTime = parser.parseStrTime(endTime)
	return entropia(contarSimbolos(dump, startTime, endTime))

if __name__ == '__main__':
	cantidad = collections.Counter()
	paramDict = parseParams(sys.argv[1:])
	if paramDict[params_timePlace] == None or paramDict[params_readTime] == None or paramDict[params_history] == None:
		l = sys.stdin.readline()
		while l:
			data = l.split()
			mensaje = reduce(lambda a, b: a+'-'+b, [data[i] for i in paramDict[params_dataPlace]])
			cantidad[mensaje] += 1
			l = sys.stdin.readline()
		print entropia(cantidad)
		print 'ahora sabés más'
		exit()
