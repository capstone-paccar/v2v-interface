"""Broadcast

This class designs a transmission and recive socket to broadcast and recive IP
Address and Port data.

Notes
-------------------------------------------------------------------------------
Created by Austin Gilbert, Aashima Mehta, and Cameron Ufland for the University
of Washington, Bothell in affiliation with PACCAR Inc.
"""

import socket

<<<<<<< HEAD
=======
FORMAT = "utf-8"
>>>>>>> 9873ea6891601e9c3b34145b4532a12ff1f9fee2
class Broadcast:
    """The class used to represent a Broadcast socket for sending or recieving.

    Attributes
    ----------
    broadcastAddress : str
        the IP address to broadcast
    port : int
        the port number to broadcast on
    version : int
        the version number to broadcast

    Methods
    -------
    rxBroadcast()
        handles recieving broadcasts
    txBroadcast()
        handles transmitting broadcasts

    """
    broadcastAddress = ''
    port = 0
    version = 0

    def __init__(self, version, port = 1200, broadcastAddress = '<broadcast>'):
        self.broadcastAddress = broadcastAddress
        self.port = port
        self.version = version

        # Sets up transmission socket
        self.tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Sets up recieving socket
        self.rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_sock.settimeout(0.2)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rx_sock.bind(('', self.port))

    #Handles the receiving of broadcasts, it adds IP addresses to the dictionary
    def rxBroadcast(self):
        """Handles recieving broadcasts.
        
        Returns
        -------
        (version, (address, port)) : tuple
            tuple object with socket information
        """
        try:
            data, addr = self.rx_sock.recvfrom(1024)
            return (str(data.decode()), addr)
        except:
            return(-1, ("", ""))

    #Handles the transmission. and then broadcasts the version number to the network.
<<<<<<< HEAD
    def txBroadcast(self):
        """Handles transmitting broadcasts."""
        self.tx_sock.sendto(bytes(str(self.version), "utf-8"), (self.broadcastAddress, self.port))
=======

    def tx_broadcast(self):
        self.tx_sock.sendto(bytes(str(self.version), FORMAT), (self.BROADCAST_ADDRESS, self.PORT))

    def close_tx_sock(self):
        self.tx_sock.close()
    
    def close_rx_sock(self):
        self.rx_sock.close()
>>>>>>> 9873ea6891601e9c3b34145b4532a12ff1f9fee2
