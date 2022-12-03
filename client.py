import socket
import threading
import os

HOST= "192.168.0.110"
PORT = 65432
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(ADDR)

    def send(msg):
        message = msg.encode(FORMAT)
        client.send(message)
        #print(client.recv(1024).decode(FORMAT))

    while True:
        os.system('cls||clear')
        msg_from_server = client.recv(1024).decode(FORMAT)
        
        if msg_from_server:
            print(msg_from_server)

        msg = input()
        send(msg)
        
        if msg == DISCONNECT_MESSAGE or msg_from_server == DISCONNECT_MESSAGE:
            break
    
    client.close()

    