import socket
import sys
import threading
from tkinter import Tk
from InterfazGrafica import InterfazGrafica

root = Tk()
InterfazGrafica(root, 50001, 50011, 1) 
root.mainloop()