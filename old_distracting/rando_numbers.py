#rando_numbers.py
# Sends a random number to a connected device via wifi. 


import socket
import random
import time
oldTime = time.time()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 15200))
s.listen(5)
clientsocket, address = s.accept()
print(f"connection from {address} has been established")

while True:
    if time.time() - oldTime > 60:
        clientsocket.send(bytes(str(random.randint(1,10)), "utf-8"))
        oldTime = time.time
        print("Hi")
s.close()