#!/usr/bin/python
import socket

s = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)
port = 5001 #same as server
host = '0.0.0.0' #0.0.0.0 catches any client tryna connect. 
#not sure why the actual IP of client wasn't working
s.bind((host, port))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print("Connection from {} has been established.".format(address))
    clientsocket.send(bytes("Hey there!!!".encode("utf-8")))
    clientsocket.close()
