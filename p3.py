import socket
import sys
import threading
from tkinter import Tk
from InterfazGraficaCliente import InterfazGraficaCliente

root = Tk()
InterfazGraficaCliente(root, 50003, 50013, 3) 
root.mainloop()