import socket

thisVersion = 1             #Version of the Pi that we are on
thisAddr = '655.322.214'    #IP Address of the Pi we are on
PORT = 15200                #global port
SIZE = 1024
FORMAT = "utf-8"

class Pi:
    self.version = 0
    self.addr = ''

    #constructor
    def __init__(self, version, addr):
        self.version = version
        self.addr = addr

    #getters
    def getVersion(self):
        return self.version

    def getIP(self):
        return self.addr

    #setters
    def setVersion(self, incomingVersion):
        self.version = incomingVersion

    def setIP(self, incomingAddr):
        self.addr = incomingAddr

#stimulate the scripts to run atleast 3 times if failing!
