#coding: utf-8

import time as tm
import sys
parseStrTime = lambda string: tm.strptime(string, '%d-%m-%y/%I:%M%p') if string else None
esValida = lambda cota, val, cmp: cota is None or cmp(cota, val)

def readFilteredLine(f, filtro):
	l = f.readline()
	while l and not filtro(l):
		if filtro(l) == None : return None
		l = f.readline()
	return l

def filtrarPorTiempo(linea, timeStart, timeEnd):
	l = linea.split() if linea else None
	if l == None or len(l) == 0 or l[0] != '1':
		#Miramos sólo who-has
		return False 
	elif len(l) < 6:
		#Si no tenemos timestamp, no filtramos
		return True
	else:
		if esValida(timeStart, parseStrTime(l[5]), lambda x,y: x<=y):
			if esValida(timeEnd, parseStrTime(l[5]), lambda x,y: x>=y):
				#timeStart <= timestamp <= timeEnd
				return True
			else:
				#me pasé, basta de buscar
				return None 
		else:
			return False


def getEdgeList(dump, timeStart= None, timeEnd = None):
	f = open(dump, 'r')
	l = readFilteredLine(f, lambda l: filtrarPorTiempo(l, timeStart, timeEnd))
	edgeList = []
	while l:
		l = l.split()
		edgeList.append((l[1], l[2]))
		l = readFilteredLine(f, lambda l: filtrarPorTiempo(l, timeStart, timeEnd))
	f.close()
	return edgeList

def grafoDeRed(dump, timeStart = None, timeEnd = None):
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

def easyPlot(g, onlyNodes = False, useLabels = [], title = None, noLayout = False):
	import matplotlib as mpl
	import networkx as nx
	mpl.use('cocoaagg')		#hack para mac
	import matplotlib.pyplot as pplot
	pplot.figure()
	if title:
		pplot.title(title)
	if onlyNodes:
		nx.draw_networkx_nodes(g, pos = logLayout(g), with_labels = useLabels, node_size = 50)
	else:
		if noLayout:
			nx.draw(g, with_labels = useLabels, node_size = 50)
		else:
			nx.draw(g, pos = logLayout(g), with_labels = useLabels, node_size = 50)
	print 'temine de calcular'
	pplot.show()
