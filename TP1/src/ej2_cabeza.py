#Script para pegar en el scapy
import sys
import datetime

def grabar(f, p):
    f.write("%d %s %s %s %s %s\n" % (p.op, p.psrc, p.pdst, p.hwsrc, p.hwdst, datetime.datetime.now().strftime("%d-%m-%y/%I:%M%p")))

dump = open('capturaTarde.data', 'w') #ojo que borra lo que habia y abre un archivo en blanco!!
escribirPaquete = lambda p: grabar(dump, p)
capturar = lambda: sniff(lfilter = lambda p: p.haslayer('ARP'), prn = lambda p: escribirPaquete(p))

#hasta aca!

#capturar() en la consola de scapy: empieza a capturar y guarda en el archivo
#lo interrumpimos con ctrl c cuando nos aburrimos, y despues  hay que hacer
dump.close()
#para que guarde todo efectivamente
