
import socket

'''it has a dictionary to store broadcasted messages that are received along with their version numbers. it uses
    sockets to send broadcast messages to all devices on the mesh network'''
# For educational purposes only. This class was made for the Spring 2021 CE/EE Capstone course at  U of WA, Bothell
#Created by Cameron in collaboration with Aashima Mehta, and Austin Gilbert

class Broadcast:
    def __init__(self, version, port = 15200, broadcast_addr = '255.255.255.255'):
        self.BROADCAST_ADDRESS = broadcast_addr
        self.PORT = port
        self.version = version
        #set up transmission socket
        self.tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #set up broadcast receive socket
        self.rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rx_sock.bind(('', self.PORT))  

    #Handles the receiving of broadcasts, it adds IP addresses to the dictionary
    def rx_broadcast(self):
        data, addr = self.rx_sock.recvfrom(1024)
        return (str(data.decode()), addr)

    #Handles the transmission. It loads the transmitting device's IP address into a dictionary and then broadcasts the version number to the network.
    def tx_broadcast(self):
        self.tx_sock.sendto(bytes(str(self.version), 'utf-8'), (self.BROADCAST_ADDRESS, self.PORT))
    
    def close_tx_sock(self):
        self.tx_sock.close()
    
    def close_rx_sock(self):
        self.rx_sock.close()