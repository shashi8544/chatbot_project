
from datetime import datetime
start_time = datetime.now()

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


########### importing libraries
import socket
import threading 
import sqlite3
import tkinter 
import tkinter.scrolledtext
from tkinter import *
from tkinter import ttk

######## host and port
HOST = socket.gethostbyname(socket.gethostname())
HOST = "192.168.56.1"
PORT = 9000

sqlite3.connect('1.db')
sqlite3.connect('2.db')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(100)
clients = []
nicknames = []


# For broadcasting messages 
def broadcast(message):
    for client in clients:
        client.send(message)
    
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# For receivng meessages 
def receive():
    while True:
        client,  address = server.accept()

        print(f"connected with {address}")
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        
        nicknames.append(nickname)
        clients.append(client)
        
        print(f" {nickname} has connected to server")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))       
        client.send("Connected to the server".encode('utf-8'))
        
        thread = threading.Thread(target =handle , args = (client,))
        thread.start()

print("Server Running")
receive()


end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
