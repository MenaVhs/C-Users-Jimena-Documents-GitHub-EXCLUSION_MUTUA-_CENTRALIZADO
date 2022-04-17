import socket
import sys
import threading
from tkinter import Tk
from InterfazServidor import InterfazServidor

root = Tk()
InterfazServidor(root, 60000)  # aquí debe escuchar a todos
root.mainloop()