
# For educational purposes only. This class was made for the Spring 2021 CE/EE Capstone course at  U of WA, Bothell
#Created by Cameron in collaboration with Aashima Mehta, and Austin Gilbert
import socket

FORMAT = "utf-8"
class Broadcast:
    BROADCAST_ADDRESS = ''
    PORT = 0
    version = 0
    def __init__(self, version, port = 1200, broadcast_addr = '<broadcast>'):
        self.BROADCAST_ADDRESS = broadcast_addr
        self.PORT = port
        self.version = version
        #set up transmission socket
        self.tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #set up broadcast receive socket
        self.rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_sock.settimeout(0.2)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rx_sock.bind(('', self.PORT))  

    #Handles the receiving of broadcasts, it adds IP addresses to the dictionary
    def rx_broadcast(self):
        try:
            data, addr = self.rx_sock.recvfrom(1024)
            return (str(data.decode()), addr)
        except:
            return(-1, ("", ""))

    #Handles the transmission. and then broadcasts the version number to the network.

    def tx_broadcast(self):
        self.tx_sock.sendto(bytes(str(self.version), FORMAT), (self.BROADCAST_ADDRESS, self.PORT))

    def close_tx_sock(self):
        self.tx_sock.close()
    
    def close_rx_sock(self):
        self.rx_sock.close()
