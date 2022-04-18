from asyncio.windows_events import NULL
from tkinter import Tk, Label, Button
import tkinter.font as tkFont
import socket
import threading

class InterfazGraficaCliente:
    NODO_SERVIDOR = 50009
    mi_id = 0
    puerto_escucha = 0
    puerto_envio = 0
    estado = []
    s = NULL
    solicita_zona1  = 'Solicita Zona Crítica 1'
    solicita_zona2 = 'Solicita Zona Crítica 2'
    saliendo_de_zona1 = 'Saliendo_de_zona 1'
    saliendo_de_zona2 = 'Saliendo_de_zona 2'
    en_zona = 'En Zona Crítica 1'
    en_zona2 = 'En Zona Crítica 2'
    sin_accion = 'Sin Acción'

    def __init__(self, master, puerto_escucha, puerto_envio, mi_id ):

        self.master = master
        self.estado = [self.sin_accion, self.sin_accion]
        self.puerto_escucha = puerto_escucha
        self.puerto_envio = puerto_envio
        self.mi_id = mi_id

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', self.puerto_envio))

        listener = threading.Thread(target=self.listen, daemon=True)
        listener.start()

        titulo = tkFont.Font(family="Arial", size=18, weight="bold", slant="italic")
        boton = tkFont.Font(family="Arial", size=16, weight="bold")
        texto = tkFont.Font(family="Arial", size=16, weight="normal")
        textoBold = tkFont.Font(family="Arial", size=16, weight="bold")

        master.title("Exclusión mutua: Algoritmo Centralizado")

        self.etiquetaProceso = Label(master, text='Proceso {}'.format(self.mi_id+1))
        self.etiquetaProceso.configure(font=titulo)
        self.etiquetaProceso.pack(padx=60,pady=10)
                
        self.etiqueta = Label(master, text="Estado:")
        self.etiqueta.configure(font=textoBold)
        self.etiqueta.pack(padx=60,pady=10)
        self.lblEstado = Label(master, text='')
        self.lblEstado.config(text=f'{self.estado[0]}, {self.estado[1]} ')
        self.lblEstado.configure(font=texto)
        self.lblEstado.pack(padx=60,pady=10)

        self.botonZonaCritica = Button(master, text="→ Solicitar Zona crítica 1", command=self.solicitar_zona1)
        self.botonZonaCritica.configure(font=boton)
        self.botonZonaCritica.pack(padx=20,pady=10)
        self.botonZonaCritica2 = Button(master, text="→ Solicitar Zona crítica 2", command=self.solicitar_zona2)
        self.botonZonaCritica2.configure(font=boton)
        self.botonZonaCritica2.pack(padx=20,pady=10)
        self.SalirSonaCritica = Button(master, text="← Salir de a Zona crítica 1", command=self.salir_de_zona1)
        self.SalirSonaCritica.configure(font=boton)
        self.SalirSonaCritica.pack(padx=20,pady=10) 
        self.SalirSonaCritica2 = Button(master, text="← Salir de a Zona crítica 2", command=self.salir_de_zona2)
        self.SalirSonaCritica2.configure(font=boton)
        self.SalirSonaCritica2.pack(padx=20,pady=10) 
    
   
    def solicitar_zona1(self):
        if self.estado[0] == self.solicita_zona1 or self.estado[0] == self.en_zona:
                return
        self.estado[0] = self.solicita_zona1
        msg =f'{str(self.mi_id)},{self.solicita_zona1}'
        self.enviar_mensaje_a_servidor(msg)
        self.actualziar_interfaz()
        

    def solicitar_zona2(self):
        if self.estado[1] == self.solicita_zona2 or self.estado[1] == self.en_zona2:
                return
        self.estado[1] = self.solicita_zona2
        msg =f'{str(self.mi_id)},{self.solicita_zona2}'
        self.enviar_mensaje_a_servidor(msg)
        self.actualziar_interfaz()

    def salir_de_zona1(self):
        if self.estado[0] == self.en_zona:
            print('saliendo de zona crítica')
            self.estado[0] = self.sin_accion
            msg =f'{str(self.mi_id)},{self.saliendo_de_zona1}'
            self.enviar_mensaje_a_servidor(msg)
            self.actualziar_interfaz()

    def salir_de_zona2(self):
        if self.estado[1] == self.en_zona2:
            self.estado[1] = self.sin_accion
            msg =f'{str(self.mi_id)},{self.saliendo_de_zona2}'
            self.enviar_mensaje_a_servidor(msg)
            self.actualziar_interfaz()
    
    def actualziar_interfaz(self):
        self.lblEstado.config(text=f'{self.estado[0]},{self.estado[1]}')
    
    def enviar_mensaje_a_servidor(self, msg):
        print(msg, '', self.NODO_SERVIDOR)
        self.s.sendto(msg.encode(), ('127.0.0.1', self.NODO_SERVIDOR))

    def listen(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', self.puerto_escucha))
        while True:
            data = sock.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')
            mensaje_recibido = data.decode()
            msg_array = mensaje_recibido.split(',')
            respuesta = msg_array[0]
            zona = msg_array[1]
            print(respuesta, zona)
            # 'ok,1'
            if respuesta == 'ok':
                if zona == '1':
                    self.estado[0] = self.en_zona
                if zona == '2':
                    self.estado[1] = self.en_zona2    
                
            self.actualziar_interfaz()