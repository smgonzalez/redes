#coding: utf-8
class Arp:
	"""Datos de captura de un paquete ARP (así no necesitamos scapy para todo esto). En realidad, tampoco lo necesitamos, me parece."""
	ipSrc = ''
	ipDst = ''
	macSrc = ''
	macDst = ''
	op = ''
	tmstmp = None

	# def __init__():
	# 	return None

	def __init__(self, linea):
		# pkg = Arp()
		dataList = linea.split()
		self.op = dataList[0]
		self.ipSrc = dataList[1]
		self.ipDst = dataList[2]
		self.macSrc = dataList[3]
		self.macDst = dataList[4]
		if len(dataList) > 5:
			import time as tm
			self.tmpstmp = tm.strptime(dataList[5], '%d-%m-%y/%I:%M%p')

	def getRel(self):
		return (self.ipSrc, self.ipDst)

import time as tm
parseStrTime = lambda string: tm.strptime(string, '%d-%m-%y/%I:%M%p')

def getEdgeList(dump, timeStart= None, timeEnd = None):
	f = open(dump, 'r')
	esValida = lambda cota, val, cmp: cota is None or cmp(cota, parseStrTime(val))  #cómo me gusta poner implicaciones en los ifs
	#l[0] = op, l[1] = ipSrc, l[2] = ipDst
	for linea in f:
		l = linea.split() 
		if l[0] == '1' and esValida(timeStart, l[5], lambda x, y: x<=y): 
			break
	edgeList = [(l[1], l[2])]
	for linea in f:
		l = linea.split()
		if l[0] == '1':
			if esValida(timeEnd, l[5], lambda x, y: x>=y):
				# ipSrc -> ipDst
				edgeList.append((l[1], l[2]))
			else:
				break
		else:
			continue
	f.close()
	return edgeList

def grafoDeRed(dump, timeStart = None, timeEnd = None, plot = False):
	import matplotlib as mpl
	import networkx as nx
	edgeList = getEdgeList(dump, timeStart, timeEnd)
	g = nx.MultiDiGraph()
	g.add_edges_from(edgeList)
	return g

def logLayout(g):
	import networkx as nx
	import math as m
	logDegree = {}
	for k, v in g.in_degree_iter():
		logDegree[k] = int(m.floor(m.log(v, 2.5))) if v > 0 else 0 #3 me pareció una buena constante, pero por ninguna razón en particular.
	deltaG = max(logDegree.itervalues())
	circulos = []
	for i in range(deltaG + 1):
		circulos.append([])
	for k, v in logDegree.iteritems():
		circulos[deltaG-v].append(k)
	for circ in circulos:
		if len(circ) == 0:
			circ.append('1')
	return nx.layout.shell_layout(g, nlist = circulos)

def easyPlot(g, onlyNodes = False):
	import matplotlib as mpl
	import networkx as nx
	mpl.use('cocoaagg')		#hack para mac
	import matplotlib.pyplot as pplot
	pplot.figure()
	if onlyNodes:
		nx.draw_networkx_nodes(g, pos = logLayout(g), useLabels = True)
	else:
		nx.draw(g, pos = logLayout(g))
	pplot.show()















