#!/usr/bin/python
import socket

#IP here is the IP address of the server
IP = '10.0.0.116' #socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    try:
        client = socket.socket()
        client.settimeout(5)
        client.connect(ADDR)
        file = open("transfer.txt", "r")
        data = file.read()

        client.send("transfer.txt".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT) 
        print("[SERVER]: {}".format(msg))

        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print("[SERVER]: {}".format(msg))

        file.close()

        client.close()
    except:
        print("Client Timeout: Couldn't connect to the server")


if __name__ == "__main__":
    main()
