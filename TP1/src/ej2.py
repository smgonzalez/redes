#!/usr/bin/python

# este script se puede correr con ./, empieza a caputar hasta que se interrumpa con ctrl + c
import sys
import datetime
import os

from scapy.all import *

DUMP_DIR='capturas'


def grabar(f, p):
    f.write("%d %s %s %s %s %s\n" % (p.op, p.psrc, p.pdst, p.hwsrc, p.hwdst, datetime.datetime.now().strftime("%d-%m-%y/%I:%M%p")))

if __name__ == '__main__':

	if os.geteuid():
		print "Vuelve cuando seas root (correr con sudo :) )"
		exit()
	
	# seteamos lugar donde se va a imprimir el archivo de salida
	if not os.path.exists(DUMP_DIR):
		os.mkdir(DUMP_DIR)

	time = datetime.datetime.now().strftime('%d%m%y-%H:%M:%S')
	filename = DUMP_DIR + '/' + time + '.data'
	dump = open(filename, 'w') 

	# Definicion de funciones para capturar mensajes ARP (sniff)
	# y para escribir lo capturado en el archivo
	escribirPaquete = lambda p: grabar(dump, p)
	capturar = lambda: sniff(lfilter = lambda p: p.haslayer('ARP'), prn = lambda p: escribirPaquete(p))

	print "Inicio de captura, para interrumpir -> ctrl + c"
	capturar()

	dump.close()
	print
	print 'Captura guardada en', filename

	exit()
