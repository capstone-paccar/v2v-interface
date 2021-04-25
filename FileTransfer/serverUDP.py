import socket
import sys

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.gethostbyname(socket.gethostname())
port = 5001
FORMAT = "utf-8"
SIZE = 1024

# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)
print("Do Ctrl+c to exit the program !!")

while True:
    print("####### Server is listening #######")
    data, addr = s.recvfrom(SIZE)
    print("[NEW CONNECTION] {} connected.".format(addr))
    print("\n\n Files are being transfered ", data.decode('utf-8'), "\n\n")
    
    #filename = conn.recv(SIZE).decode(FORMAT)
    print("[RECV] Receiving the filename.")
    file = open("client.txt", "w")

    print("[RECV] Receiving the file data.")

    try:
        while(data):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            file.write(data)
            data, addr = s.recvfrom(SIZE)
    except:
        file.close()
        s.close()

    file.close()
    s.close()
    print("[DISCONNECTED] {} Download complete.".format(addr))

