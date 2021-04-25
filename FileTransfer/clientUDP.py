import socket
import sys

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
ip = socket.gethostbyname(socket.gethostname())
port = 5001
addr = (ip,port)
FORMAT = "utf-8"
SIZE = 1024
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
while True:
    send_data = input("Do you wish to download files? Y/N =>")
    if(send_data == 'Y' or send_data == 'y'):
        s.sendto(send_data.encode('utf-8'), (ip, port))
        print("\nDownloading in progress\n")
        file = open("transfer.txt", "r")
        data = file.read(SIZE)

        s.sendto("client.txt".encode(FORMAT), addr)
        
        while(data):
            if(s.sendto("transfer.txt".encode(FORMAT),addr)):
                print("\nsending...")
                data = file.read(SIZE)

        file.close()
        print("DOWNLOAD COMPLETE!")
        s.close()
        break
    else:
        s.close()
        break
# close the socket
s.close()