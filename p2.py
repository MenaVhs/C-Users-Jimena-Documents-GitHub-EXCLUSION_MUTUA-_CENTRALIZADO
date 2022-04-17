import socket
import sys
import threading
from tkinter import Tk
from InterfazGraficaCliente import InterfazGraficaCliente

root = Tk()
InterfazGraficaCliente(root, 50002, 50009, 1) 
root.mainloop()