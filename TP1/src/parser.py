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
