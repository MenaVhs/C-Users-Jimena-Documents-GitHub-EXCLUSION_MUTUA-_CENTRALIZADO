from asyncio.windows_events import NULL
from tkinter import Tk, Label
import tkinter.font as tkFont
import socket
import sys
import threading

from pyparsing import col

class InterfazServer:
    PUERTOS_CLIENTES = [0,50001,50002,50003,50004,50005,50006]
    mi_id = 0
    puerto_escucha = 0
    puerto_envio = 0

    zona_1 = NULL #guarda el id del proceso que está en zona
    zona_2 = NULL

    #estado = []
    cola_zona_1 = []
    cola_zona_2 = []

    s = NULL
    #permiso = NULL

    #nomenclatura
    solicita_zona1  = 'Solicita Zona Crítica 1'
    solicita_zona2 = 'Solicita Zona Crítica 2'
    saliendo_de_zona1 = 'Saliendo_de_zona 1'
    saliendo_de_zona2 = 'Saliendo_de_zona 2'


    def __init__(self, master, puerto_escucha, puerto_envio, mi_id):
        self.master = master
        self.zona_1 = ''
        self.zona_2 = ''
        
        self.puerto_escucha = puerto_escucha
        self.puerto_envio = puerto_envio
        self.mi_id = mi_id
    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', self.puerto_envio))

        listener = threading.Thread(target=self.listen, daemon=True)
        listener.start()

    #ventana
        titulo = tkFont.Font(family="Arial", size=18, weight="bold", slant="italic")
        texto = tkFont.Font(family="Arial", size=16, weight="normal")
        textoBold = tkFont.Font(family="Arial", size=16, weight="bold")

        master.title("Servidor")

        self.etiquetaProceso = Label(master, text = 'Servidor')
        self.etiquetaProceso.configure(font=titulo)
        self.etiquetaProceso.pack(padx=60,pady=10)


        self.lbl_titulo_zona1 = Label(master, text="Ocupación de Zona 1:")
        self.lbl_titulo_zona1.config(font=titulo)
        self.lbl_titulo_zona1.pack(padx=20,pady=10)
        self.lbl_zona1 = Label(master, text=self.zona_1)
        self.lbl_zona1.config(font=titulo)
        self.lbl_zona1.pack(padx=20,pady=10)

        self.cola1 = Label(master, text="Cola Zona Crítica 1[]")
        self.cola1.configure(font=texto)
        self.cola1.pack(padx=20,pady=10)

        self.lbl_titulo_zona2 = Label(master, text="Ocupación de Zona 2:")
        self.lbl_titulo_zona2.config(font=titulo)
        self.lbl_titulo_zona2.pack(padx=20,pady=10)
        self.lbl_zona2 = Label(master, text=self.zona_2)
        self.lbl_zona2.config(font=titulo)
        self.lbl_zona2.pack(padx=20,pady=10)

        self.cola2 = Label(master, text="Cola Zona Crítica 2[]")
        self.cola2.configure(font=texto)
        self.cola2.pack(padx=20,pady=10)
        
 
    def actualziar_interfaz(self):
        self.lbl_zona1.config(text = f'{str(self.zona_1)}')
        self.lbl_zona2.config(text = f'{str(self.zona_2)}')
        
        self.cola1.config(text = f'Lista de cola 1: {self.cola_zona_1}')
        self.cola2.config(text = f'Lista de cola 2: {self.cola_zona_2}')   

    def responder_ok(self,msg, id_proceso):
        self.s.sendto(msg.encode(), ('127.0.0.1', self.PUERTOS_CLIENTES[int(id_proceso)]))

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', self.puerto_escucha))
        
        while True:
            data = sock.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')
            mensaje_recibido = data.decode()
            # '0,Solicita Zona Crítica 1'
            msg_array = mensaje_recibido.split(',')
            id_solicitante = msg_array[0]
            accion_solicitante = msg_array[1]
            if accion_solicitante == self.solicita_zona1:
                if self.zona_1 == '':
                    self.zona_1 = id_solicitante
                    msg = 'ok,1'
                    self.responder_ok(msg, id_solicitante)
                else:
                    self.cola_zona_1.append(int(id_solicitante))
            if accion_solicitante == self.solicita_zona2:
                if self.zona_2 == '':
                    self.zona_2 = id_solicitante
                    msg = 'ok,2'
                    self.responder_ok(msg, id_solicitante)
                else:
                    self.cola_zona_2.append(int(id_solicitante))

            if accion_solicitante == self.saliendo_de_zona1:
                self.zona_1 = ''
                if len(self.cola_zona_1) > 0:
                    self.zona_1 = self.cola_zona_1.pop(0)
                    print('pop: ',self.zona_1)
                    msg = 'ok,1'
                    self.responder_ok(msg, self.zona_1)

            if accion_solicitante == self.saliendo_de_zona2:
                self.zona_2 = ''
                if len(self.cola_zona_2) > 0:
                    self.zona_2 = self.cola_zona_2.pop(0)
                    msg = 'ok,2'
                    self.responder_ok(msg, self.zona_2)    

            self.actualziar_interfaz()
