#coding: utf-8
import matplotlib as mpl
import networkx as nx
mpl.use('cocoaagg')		#hack para mac
import matplotlib.pyplot as pplot

def separarData(dataYLabels):
	data = []
	labels = []
	for (label, datum) in dataYLabels:
		data.append(datum)
		labels.append(label)
	return data, labels


	pplot.figure()
def plotBars(data, labels, title, horizontalLine = None, widthLevel = 1, verticalLine = None):
	import numpy.numarray as na
	xlocations = na.array(range(len(data)/widthLevel))+0.5
	width = 0.5 * widthLevel
	pplot.bar(xlocations, data, width=width, color = 'g')
	pplot.xticks(xlocations-1.5*width, labels, rotation = 30, fontsize = 12)
	pplot.xlim(0, xlocations[-1]+width*2)
	pplot.title(title)
	if horizontalLine:
		pplot.axhline(linewidth=2, color='r', y = horizontalLine) 
	if verticalLine:
		pplot.axvline(linewidth=2, color='r', x = verticalLine) 
	pplot.gca().get_xaxis().tick_bottom()
	pplot.gca().get_yaxis().tick_left()
	# pplot.show()


# pplot.figure()
# pplot.title('Red ISP: Cantidad de apariciones por mensaje. Histograma normalizado.')
# pplot.hist(cantsTardeFit, bins = 200, normed = True)
# pplot.ylabel('frecuencia relativa')
# pplot.xlabel('cantidad de apariciones por mensaje')
# pplot.show()

import Entropimetro as ep

def infoPorHost(dump, nombreDeRed):
	entropia = ep.calcularTodo(dump)
	data = ep.calcularInfoPorHost(dump).values()
	data.sort()
	plotBars(
		data, 
		labels = [], 
		title = (nombreDeRed if nombreDeRed else '') + u"Información por host y entropía general",
		horizontalLine = entropia,
	)
	pplot.xlabel('Hosts')
	pplot.ylabel(u"Cantidad de información (bits)")

import parser as *

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



