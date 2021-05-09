#!/usr/bin/python
import socket

IP = '0.0.0.0' #gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    print("[STARTING] Server is starting.")
    server = socket.socket() #(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print("[LISTENING] Server is listening.")

    while True:
        conn, addr = server.accept()
        print("[NEW CONNECTION] {} connected.".format(addr))
        filename = conn.recv(SIZE).decode(FORMAT)
        print("[RECV] Receiving the filename.")
        file = open(filename, "w")
        conn.send("Filename received.".encode(FORMAT))

        data = conn.recv(SIZE).decode(FORMAT)
        print("[RECV] Receiving the file data.")
        file.write(data)
        conn.send("File data received".encode(FORMAT))

        file.close()

        conn.close()
        print("[DISCONNECTED] {} disconnected.".format(addr))

if __name__ == "__main__":
    main()
