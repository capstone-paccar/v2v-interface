"""Pi

This class designs a Pi object to store and set a version number and IP addresses.

Notes
-------------------------------------------------------------------------------
Created by Austin Gilbert, Aashima Mehta, and Cameron Ufland for the University
of Washington, Bothell in affiliation with PACCAR Inc.
"""

class Pi:
    """The class used to represent a Pi.

    Attributes
    ----------
    version : int
        the version number of the Pi
    address : str
        the IP address of the Pi

    Methods
    -------
    getVersion()
        the getter for the Pi's version number
    getIP()
        the getter for the Pi's IP address
    setVersion()
        the setter for the Pi's version number
    setIP()
        the setter for the Pi's IP address
    """
    
    version = 0
    address = ''

    def __init__(self, version, address):
        self.version = version
        self.address = address

    def getVersion(self):
        """The getter for the Pi's version number."""
        return self.version

    def getIP(self):
        """The getter for the Pi's IP address."""
        return self.address

    def setVersion(self, incomingVersion):
        """The setter for the Pi's version number."""
        self.version = incomingVersion

    def setIP(self, incomingaddress):
        """The setter for the Pi's IP address."""
        self.address = incomingaddress