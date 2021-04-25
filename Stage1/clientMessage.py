#!/usr/bin/python
import socket

s = socket.socket() #socket.AF_INET, socket.SOCK_STREAM
port = 5001 #port must be same for client and server
host = '10.0.0.1' #server's IP adr
s.connect((host, port))

full_msg = ''
while True:
    msg = s.recv(8)
    if len(msg) <= 0:
        break
    full_msg += msg.decode("utf-8")

print(full_msg)
