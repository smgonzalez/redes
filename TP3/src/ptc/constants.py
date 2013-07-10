# -*- coding: utf-8 -*- 
# # # # # # # # # # # # # # # # # # # # #
#                                       #                                       
#    Trabajo Práctico 3 - Conexiones    # 
#                                       #
#     Teoría de las Comunicaciones      #
#      Departamento de Computación      #
#              FCEN - UBA               #
#            junio de 2013              #
#                                       #
# # # # # # # # # # # # # # # # # # # # #


PROTOCOL_NUMBER = 202

MIN_PACKET_SIZE = 1
MAX_PACKET_SIZE = 1000

RETRANSMISSION_TIMEOUT = 2
MAX_RETRANSMISSION_ATTEMPTS = 10

SERVER_CONNECTION_TIMEOUT = 40

MAX_SEQ = (1<<16) - 1
MAX_ACK = (1<<16) - 1
SEND_WINDOW = 10
RECV_WINDOW = 1

SYN_SENT = 1
SYN_RECEIVED = 2
ESTABLISHED = 3
FIN_SENT = 4
FIN_RECEIVED = 5
CLOSED = 6

DEBUG = True
RANDOM_LOSS = True #el sender pierde paquetes a propósito (sólo funciona con debug = True)