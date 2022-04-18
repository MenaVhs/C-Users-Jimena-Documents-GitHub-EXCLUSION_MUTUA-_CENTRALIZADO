import socket
import sys
import threading
from tkinter import Tk
from InterfazServer import InterfazServer

root = Tk()
InterfazServer(root, 50009, 50019, 99)  # aquí debe escuchar a todos
root.mainloop()