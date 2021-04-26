#!/usr/bin/python
import socket
import sys

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
ip = '10.0.0.116' #socket.gethostbyname(socket.gethostname())
port = 6000
addr = (ip,port)
FORMAT = "utf-8"
SIZE = 1024

filename = "transfer.txt"
s.sendto(filename, (ip, port))
print("Sending {} ... ".format(filename))
f = open(filename, "r")
data = f.read(1024)

# Let's send data through UDP protocol
while (data):
    if(s.sendto(data, (ip,port))):
        data = f.read(1024)
    
s.close()
f.close()
print("File transfer via UDP complete")

