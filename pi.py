class Pi:
    version = 0
    addr = ''

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