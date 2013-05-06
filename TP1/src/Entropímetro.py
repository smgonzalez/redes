#!/usr/bin/python
#coding: utf-8

import sys

import sys
import datetime
import os
import re
import collections
import math

params_readTime  = 'readtime'
params_timePlace = 'timeplace'
params_history = 'history' #en minutos
params_dataPlace = 'dataplace'

params = {params_readTime : None,
	params_timePlace : None,
	params_history: None,
	params_dataPlace : None,
}

def parseParams(args):
	argString = reduce(lambda a, b: a+' '+b, args)
	paramDict = {}
	for paramKey in params.iterkeys():
		regex = re.compile('(?:.+?|^)--'+paramKey+'\s*=\s*(?P<'+paramKey+'>.+?)(?:\s|$)') #odio las expresiones regulares profundamente
		valor = regex.match(argString)
		if (valor):
			paramDict.update(valor.groupdict())
	for k, v in paramDict.iteritems():
		if k == params_readTime or k == params_history:
			paramDict[k] = int(v)
		elif k == params_dataPlace:
			paramDict[k] = map(int, v.split(','))
	return paramDict

def entropia(counter):
	total = float(sum(counter.values()))
	ponderacion = lambda s: counter[s]/total * (math.log(total/counter[s]))
	return sum(map(ponderacion, counter.iterkeys()))

if __name__ == '__main__':
	cantidad = collections.Counter()
	paramDict = parseParams(sys.argv[1:])
	if paramDict[params_timePlace] == None or paramDict[params_readTime] == None or paramDict[params_history]:
		l = sys.stdin.readline()
		while l:
			data = l.split()
			mensaje = reduce(lambda a, b: a+'-'+b, [data[i] for i in paramDict[params_dataPlace]])
			cantidad[mensaje] += 1
			l = sys.stdin.readline()
		print entropia(cantidad)
		print 'ahora sabés más'
		exit()
