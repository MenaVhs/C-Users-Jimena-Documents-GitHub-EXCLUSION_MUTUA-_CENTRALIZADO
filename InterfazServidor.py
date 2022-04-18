from asyncio.windows_events import NULL
from tkinter import Tk, Label
import tkinter.font as tkFont
import socket
import sys
import threading

class InterfazServidor:
    NODO_SERVIDOR = 50009
    NODOS_ENVIO = [50001,50002,50003,50004,50005,50006]

    puerto_escucha = 0
    puerto_envio = 0

    estado = []
    cola_zona_1 = []
    cola_zona_2 = []

    sock = NULL
    permiso = NULL

    solicita_zona  = 'Solicita Zona Crítica 1'
    solicita_zona2 = 'Solicita Zona Crítica 2'
    en_zona = 'En Zona Crítica 1'
    en_zona2 = 'En Zona Crítica 2'
    sin_accion = 'Sin Acción'
 

    def __init__(self, master, puerto_escucha):
        self.estado = [self.sin_accion,self.sin_accion]

        self.puerto_escucha = puerto_escucha
        # self.puerto_envio = puerto_envio
        # self.mi_id = mi_id-1
    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', self.puerto_envio))

        listener = threading.Thread(target=self.listen, daemon=True)
        listener.start()
        self.master = master

        titulo = tkFont.Font(family="Arial", size=18, weight="bold", slant="italic")
        texto = tkFont.Font(family="Arial", size=16, weight="normal")
        textoBold = tkFont.Font(family="Arial", size=16, weight="bold")

        master.title("Servidor")

        self.etiquetaProceso = Label(master, text = 'Servidor')
        self.etiquetaProceso.configure(font=titulo)
        self.etiquetaProceso.pack(padx=60,pady=10)


        # Las colas las almacena el servidor
        
        self.Estado = Label(master, text = "Estado")
        self.Estado.configure(font=textoBold)
        self.Estado.pack(padx=60,pady=10)
        self.lblEstado = Label(master, text='')
        self.lblEstado.config(text=f'{self.estado[0]},{self.estado[1]}')
        self.lblEstado.configure(font=texto)
        self.lblEstado.pack(padx=60,pady=10)


        self.cola1 = Label(master, text="Cola Zona Crítica 1[]")
        self.cola1.configure(font=texto)
        self.cola1.pack(padx=20,pady=10)
        self.cola2 = Label(master, text="Cola Zona Crítica 2[]")
        self.cola2.configure(font=texto)
        self.cola2.pack(padx=20,pady=10)
        
        self.lbl_permiso = Label(master, text="En Zona Crítica 1: ")
        self.lbl_permiso.configure(font=texto)
        self.lbl_permiso.pack(padx=20,pady=10)

        self.lbl_permiso2 = Label(master, text="En Zona Crítica 2: ")
        self.lbl_permiso2.configure(font=texto)
        self.lbl_permiso2.pack(padx=20,pady=10)
 
    def actualziar_interfaz(self):
        self.lblEstado.config(text=f'{self.estado[0]},{self.estado[1]}')
        self.cola1.config(text = f'Lista de cola 1: {self.cola_zona_1}')
        self.cola2.config(text = f'Lista de cola 2: {self.cola_zona_2}')   
        self.lbl_permiso.config(text=f'Está: {self.mi_id}') #duda, de dónde saco el id del proceso
        self.lbl_permiso2.config(text=f'Está: {self.mi_id}') #duda, de dónde saco el id del proceso

    def listen(self): #idC = 0, acción(SOLIZ, SALGOZ) = 1, NUMERO ZONA = 2)
        sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockServer.bind(('127.0.0.1', self.puerto_escucha))

        while True:
            sock = sockServer.accept()
            while True:
                data = sock.recv(1024).decode()
                #print('\rpeer: {}\n> '.format(data.decode()), end='')
                msg_rep = data.decode()
                msg_array = msg_rep.split(',')
                m_id_proceso_remitente = msg_array[0] # idC = 0
                m_zona_pedida = msg_array[2]
                if m_zona_pedida == '1': #zona uno
                    if msg_array[1] == self.solicita_zona:
                        # si hay un proceso en zona1, server pone en cola
                        if  self.estado[0] == self.en_zona:
                            return
                        print('encola')
                        self.cola_zona_1.append(int(m_id_proceso_remitente)+ 1 )
                        self.actualziar_interfaz()

                        # si no hay proceso en zona1, server mete proceso a zona1
                        if self.estado[0] == self.sin_accion:
                            self.estado[0] = m_id_proceso_remitente 
                            msg =f'{str(self.mi_id)}, ok , {m_zona_pedida}'
                            self.sock.sendto(msg.encode(), ('127.0.0.1', self.NODOS_ENVIO[int(m_id_proceso_remitente)]))  
                    return
                                       
                self.actualziar_interfaz()