import socket
import sys
import threading
from tkinter import Tk
from InterfazGraficaCliente import InterfazGraficaCliente

root = Tk()
InterfazGraficaCliente(root, 50006, 50016, 6) 
root.mainloop()