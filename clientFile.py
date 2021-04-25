#!/usr/bin/python
import socket

#IP here is the IP address of the server
IP = '10.0.0.116'#socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)

    client.connect(ADDR)

    file = open("transfer.txt", "r")
    data = file.read()

    client.send("transfer.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT) #decode = 'utf-8' try!
    print("[SERVER]: {}".format(msg))

    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print("[SERVER]: {}".format(msg))

    file.close()

    client.close()


if __name__ == "__main__":
    main()
