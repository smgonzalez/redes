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


import threading
import random

from common import PacketBuilder, ProtocolControlBlock
from soquete import Soquete
from packet import ACKFlag, FINFlag, SYNFlag
from worker import ClientProtocolWorker
from buffers import DataBuffer, RetransmissionQueue, NotEnoughDataException
from constants import MIN_PACKET_SIZE, MAX_PACKET_SIZE, CLOSED,\
                      ESTABLISHED, FIN_SENT, SYN_SENT, MAX_SEQ,\
                      SEND_WINDOW, MAX_RETRANSMISSION_ATTEMPTS,\
                      DEBUG, RANDOM_LOSS
from collections import Counter
                 


class ClientControlBlock(ProtocolControlBlock):
    
    def __init__(self, address, port):
        ProtocolControlBlock.__init__(self, address, port)
        # Tamaño de la ventana de emisión
        self.send_window = SEND_WINDOW
        self.reset_numbers()
            
    def get_send_seq(self):
        return self.send_seq
    
    def get_send_window(self):
        return self.send_window
    
    #############################
    ### Completar esta clase! ###
    #############################
    
    def is_inside_window(self, seqNr):
        if self.window_lo < self.window_hi:
            return self.window_lo <= seqNr < self.window_hi
        else:
            return self.window_lo <= seqNr or seqNr < self.window_hi

    # Responde True sii la ventana de emisión no está saturada.
    def send_allowed(self):
        return self.is_inside_window(self.send_seq)

    # Estas funciones las agregue yo (vicky)
    # Responde True si el ACK fue aceptado (lo que quiera que quiere decir eso).
    def ack_accepted(self, packet):
        return self.is_inside_window(packet.get_ack_number())

    # Reajusta la ventana, dado un ACK aceptado.
    def adjust_window(self, packet):
        self.window_lo = packet.get_ack_number() + 1
        self.window_hi = self.modular_sum(self.window_lo, self.send_window)
        self.send_seq = max(self.send_seq, self.window_lo)

    def increment_send_seq(self):
        self.send_seq = self.modular_increment(self.send_seq)

    def reset_numbers(self):
        # Próximo SEQ a enviar
        self.send_seq = random.randint(1, MAX_SEQ)
        # Límite inferior de la ventana (i.e., unacknowledged)
        self.window_lo = self.send_seq
        # Límite superior de la ventana
        self.window_hi = self.modular_sum(self.window_lo, self.send_window)
                

class PTCClientProtocol(object):
    
    def __init__(self, address, port):
        self.retransmission_queue = RetransmissionQueue(self)
        self.retransmission_attempts = Counter()
        self.outgoing_buffer = DataBuffer()
        self.state = CLOSED
        self.control_block = ClientControlBlock(address, port)
        self.socket = Soquete(address, port)
        self.packet_builder = PacketBuilder(self)
    
    def is_connected(self):
        return self.state == ESTABLISHED
        
    def build_packet(self, payload=None, flags=None):
        seq = self.control_block.get_send_seq()
        if payload is not None:
            self.control_block.increment_send_seq()
        packet = self.packet_builder.build(payload=payload, flags=flags, seq=seq)
        return packet
        
    def send_packet(self, packet):
        if DEBUG and RANDOM_LOSS:
            #'perdemos' un 10% de los paquetes
            if random.choice(range(10)) :
                print 'mando el paquete:', packet.get_seq_number()
                self.socket.send(packet)
            else:
                print 'Mala leche con el', packet.get_seq_number()
        else:
            self.socket.send(packet)
        
    def send_and_queue_packet(self, packet):
        self.send_packet(packet)
        self.retransmission_queue.put(packet)
        
    def send(self, data):
        if not self.is_connected():
            raise Exception('cannot send data: connection not established')
        self.worker.send(data)

    def connect_to(self, address, port):
        self.worker = ClientProtocolWorker.spawn_for(self)
        self.worker.start()
        self.connected_event = threading.Event()
        self.control_block.reset_numbers()
        self.control_block.set_destination_address(address)
        self.control_block.set_destination_port(port)
        
        syn_packet = self.build_packet(flags=[SYNFlag])
        self.send_and_queue_packet(syn_packet)
        self.state = SYN_SENT
        
        self.connected_event.wait()
    
    def handle_timeout(self):
        ###################
        ##   Completar!  ##
        ###################
        
        # Tener en cuenta que se debe:
        # (1) Obtener los paquetes en self.retranmission_queue
        # (2) Volver a enviarlos
        # (3) Reencolarlos para otra eventual retransmisión
        # ...y verificar que no se exceda la cantidad máxima de reenvíos!
        # (hacer self.shutdown() si esto ocurre y dejar un mensaje en self.error)
        
        # *** NO SE SI NO HABIA YA OTRA VARIABLE DONDE SE INDICABA LA CANTIDAD DE TRANSMISIONES
        # *** SE CUENTA POR PAQUETE O LA COLA ENTERA?
        # *** HAY QUE RETRANSMITIR TODO LO QUE ESTA EN LA COLA?
        # Cantidad maxima de reenvios: MAX_RETRANSMISSION_ATTEMPTS
        if DEBUG: print 'TIMEOUT'
        oldQueue = self.retransmission_queue
        self.retransmission_queue = RetransmissionQueue(self)       
        for packet in oldQueue:
            if self.retransmission_attempts[packet.get_seq_number()] == MAX_RETRANSMISSION_ATTEMPTS :
                self.error = 'Retransmition Limit Exceeded'
                self.shutdown()
            else:
                self.retransmission_attempts[packet.get_seq_number()] += 1
                self.send_and_queue_packet(packet) 

    def handle_pending_data(self):
        more_data_pending = False
        
        if self.control_block.send_allowed():
            try:
                data = self.outgoing_buffer.get(MIN_PACKET_SIZE, MAX_PACKET_SIZE)
            except NotEnoughDataException:
                pass
            else:
                packet = self.build_packet(payload=data)
                self.send_and_queue_packet(packet)
                
            if not self.outgoing_buffer.empty():
                more_data_pending = True
        else:
            more_data_pending = True
        
        if more_data_pending:
            self.worker.signal_pending_data()
    
    
    def handle_incoming(self, packet):
        ###################
        ##   Completar!  ##
        ###################
        
        # Tener en cuenta que se debe:
        # * Corroborar que el flag de ACK esté seteado
        # * Distinguir el caso donde el estado es SYN_SENT
        #   * No olvidar de hacer self.connected_event.set() al confirmar el ACK y establecer la conexión!!!
        # * Analizar si #ACK es aceptado (hablar con el bloque de control para hacer este checkeo)
        # * Sacar de la cola de retransmisión los paquetes reconocidos por #ACK
        # * Ajustar la ventana deslizante con #ACK
        # * Tener en cuenta también el caso donde el estado es FIN_SENT
        
        # Corroboro que el flag de ACK este seteado
        if not ACKFlag in packet:
            raise Exception('Error (hay que hacer algo mas? Es un error?)')
            self.shutdown()
            return
            
        if DEBUG: print 'me llegó el paquete numero:', packet.get_ack_number()
        # Reviso si el ACK es aceptado
        if self.control_block.ack_accepted(packet): 
            # *** Si no es aceptado no hago nada no?
            for ackedPacket in self.retransmission_queue.acknowledge(packet):
                del(self.retransmission_attempts[ackedPacket.get_seq_number()])
            self.control_block.adjust_window(packet)
        else:
            return
 
        # Si fue aceptado, ejecuto accion en base al estado actual
        # *** ASUMO QUE NO SE LO LLAMA SI EL ESTADO ES CLOSED, ESO ESTARA BIEN?
        if self.state == ESTABLISHED:
            return
        elif self.state == SYN_SENT:
            # El servidor establecio una conexion: 
            # cambio el estado del cliente y sincronizo la conexion
            
            # Corroboro que el numero de ACK recibido sea igual al numero de SEQ enviado
            ackNum = packet.get_ack_number()
            seqNum = self.control_block.get_send_seq()
            
            if not (self.control_block.modular_increment(ackNum) == seqNum):
                #self.error = 'SYN_ACK inválido'
                #self.shutdown()
                if DEBUG: print 'recibí fruta (ack != seq):', ackNum, seqNum
                #no hagamos que se cierre, tal vez le llegó algo viejo o equivocado
                #dejemos que si posta anda mal, lo maten los timeouts.
                return
            
            self.state = ESTABLISHED
            self.connected_event.set()
            if DEBUG: print 'conexión establecida'
            
        elif self.state == FIN_SENT:
            # Recibi respuesta del servidor indicando que puedo cerrar la conexion
            if DEBUG: print 'llego el fin'
            self.state = CLOSED
            # *** Hago algo mas para cerrar la conexion?
            self.shutdown() #(?)
            
        else:
            self.error = 'Estado inexistente'
            self.shutdown()
            
    def handle_close_connection(self):
        if not self.outgoing_buffer.empty():
            self.worker.signal_pending_data()
            self.worker.signal_close_connection()
        elif not self.retransmission_queue.empty():
            self.worker.signal_close_connection()
        else:
            fin_packet = self.build_packet(flags=[FINFlag])
            self.send_and_queue_packet(fin_packet)
            self.state = FIN_SENT
        
    def close(self):
        if self.is_connected():
            self.worker.signal_close_connection()
        
    def shutdown(self):
        self.outgoing_buffer.clear()
        self.retransmission_queue.clear()
        self.retransmission_attempts.clear()
        self.worker.stop()
        # Esto es por si falló el establecimiento de conexión (para destrabar al thread principal)
        self.connected_event.set()
        self.state = CLOSED
