from asyncio.windows_events import NULL
from tkinter import Tk, Label, Button
import tkinter.font as tkFont
import socket
import sys
import threading

class InterfazGrafica:
    NODOS_ENVIO = [50001,50002,50003,50004,50005,50006]
    mi_id = 0
    puerto_escucha = 0
    puerto_envio = 0
    estado = NULL
    cola_zona_1 = []
    cola_zona_2 = []
    sock = NULL
    coordinador = 'coordinador'
    solicita_zona  = 'Solicita Zona Crítica 1'
    solicita_zona2 = 'Solicita Zona Crítica 2'
    en_zona = 'En Zona Crítica 1'
    en_zona2 = 'En Zona Crítica 2'
    sin_accion = 'Sin Acción'

    permiso = NULL
    con_permiso = 'Permiso'
    sin_permiso = 'Sin Permiso'


    def __init__(self, master, puerto_escucha,puerto_envio, mi_id ):

        self.estado = self.sin_accion
        self.permiso = self.sin_accion
        self.puerto_escucha = puerto_escucha
        self.puerto_envio = puerto_envio
        self.mi_id = mi_id - 1 #

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', self.puerto_envio))

        listener = threading.Thread(target=self.listen, daemon=True)
        listener.start()
        self.master = master

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
        self.lblEstado.config(text=f'{self.estado}')
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
    
    def permiso1(self):
        pass
    
    def solicitar_zona1(self):
        pass

    def solicitar_zona2(self):
        pass

    def salir_de_zona1(self):
        pass

    def salir_de_zona2(self):
        pass

    def listen(self):
        pass