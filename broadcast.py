
import socket
"""This class is designed to operate via threading so that transmitting and receiving can occur at the same time. 
    it has a dictionary to store broadcasted messages that are received along with their version numbers. it uses
    sockets to send broadcast messages to all devices on the mesh network"""
# For educational purposes only. This class was made for the Spring 2021 CE/EE Capstone course at  U of WA, Bothell
#Created by Cameron in collaboration with Aashima Mehta, and Austin Gilbert

class Broadcast:
    nodeDict = dict()
    BROADCAST_ADDRESS = '255.255.255.255'
    PORT = 15200
    
    #Handles the receiving of broadcasts, it adds IP addresses to the dictionary
    def rx_broadcast(self):
        rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rx_socket.bind(('', self.PORT))
        rx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            data, addr = rx_socket.recvfrom(1024)
            self.nodeDict.update({addr[0] : str(data.decode())})
        rx_socket.close()
    #Handles the transmission. It loads the transmitting device's IP address into a dictionary and then broadcasts the version number to the network.
    def tx_broadcast(self, version):
        tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.nodeDict.update({tx_socket.gethostbyname(tx_socket.gethostname()): version })
        while True:
            tx_socket.sendto(bytes(str(version), 'utf-8'), (self.BROADCAST_ADDRESS, self.PORT))
        tx_socket.close()