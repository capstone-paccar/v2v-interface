"""Broadcast

This class designs a transmission and receive socket to broadcast and receive IP
Address and Port data.

Notes
-------------------------------------------------------------------------------
Created by Austin Gilbert, Aashima Mehta, and Cameron Ufland for the University
of Washington, Bothell in affiliation with PACCAR Inc.
"""

import socket

class Broadcast:
    """The class used to represent a Broadcast socket for sending or receiving.

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
        handles receiving broadcasts
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
        
        # Sets up receiving socket
        self.rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_sock.settimeout(0.2)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rx_sock.bind(('', self.port))

    def rxBroadcast(self):
        """Handles receiving broadcasts.
        
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

    def txBroadcast(self):
        """Handles transmitting broadcasts."""
        self.tx_sock.sendto(bytes(str(self.version), "utf-8"), (self.broadcastAddress, self.port))
