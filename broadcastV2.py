
import socket

'''This class is designed to operate via threading so that transmitting and receiving can occur at the same time. 
    it has a dictionary to store broadcasted messages that are received along with their version numbers. it uses
    sockets to send broadcast messages to all devices on the mesh network'''
# For educational purposes only. This class was made for the Spring 2021 CE/EE Capstone course at  U of WA, Bothell
#Created by Cameron in collaboration with Aashima Mehta, and Austin Gilbert

thisVersion = 1             #Version of the Pi that we are on
thisAddr = '655.322.214'    #IP Address of the Pi we are on
PORT = 15200                #global port
SIZE = 1024
FORMAT = "utf-8"

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

#stimulate the scripts to run atleast 3 times if failing!
def callOtherScripts(hasUpdate, needUpdate):
    times = 0 
    print("Inside the callOtherScript")
    while(times < 3):
        if(runServer(hasUpdate) and runClient(needUpdate)):
            #update the Version of the Client
            needUpdate.setVersion(hasUpdate.getVersion())
            print("Client Version : ", needUpdate.getVersion())
            break
        else:
            times = times + 1
    return

#runServer will run the server.py script on pi --> code in "server.py"
def runServer(needUpdate):
    print("Running server " + needUpdate.getIP())
    print("Server Version : ", needUpdate.getVersion())
    try:
        serverAddr = (needUpdate.getIP(), PORT)
        print("[STARTING] Server is starting.")
        server = socket.socket() #(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(serverAddr)
        server.listen(1)
        print("[LISTENING] Server is listening.")

        while True:
            conn, connaddr = server.accept()
            print("[NEW CONNECTION] {} connected.".format(connaddr))
            filename = conn.recv(SIZE).decode(FORMAT)
            print("[RECV] Receiving the filename.")
            file = open(filename, "w")
            conn.send("Filename received.".encode(FORMAT))

            data = conn.recv(SIZE).decode(FORMAT)
            print("[RECV] Receiving the file data.")
            file.write(data)
            conn.send("File data received".encode(FORMAT))

            file.close()

            conn.close()
            print("[DISCONNECTED] {} disconnected.".format(connaddr))
            return True
    except:
        return False

#runClient will run the client.py script on pi --> code in "client.py"
def runClient(hasUpdate):
    print("Running client " + hasUpdate.getIP())
    print("Client Version : ", hasUpdate.getVersion())
    try:
        clientAddr = (hasUpdate.getIP(), PORT)
        client = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)

        client.connect(clientAddr)

        file = open("transfer.txt", "r")
        data = file.read()

        client.send("transfer.txt".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT) #decode = 'utf-8' try!
        print("[SERVER]: {}".format(msg))

        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print("[SERVER]: {}".format(msg))

        file.close()

        client.close()
        return True
    except:
        return False


class Broadcast:
    BROADCAST_ADDRESS = '255.255.255.255'
    PORT = 15200

    #Handles the receiving of broadcasts, it adds IP addresses to the dictionary
    def rx_broadcast(self, version):
        print("RX_BROAD\n")
        rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rx_socket.bind(('', self.PORT))
        rx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            rx_data, rx_addr = rx_socket.recvfrom(1024)
            rx_version = str(rx_data.decode())
        #CAMERON -------------------- STIMULATE otherVersion and otherAddr------------------ '''
            #dummy otherVersion and otherAddr
            otherPi = Pi(rx_version, rx_addr[0])
            #compare versions start
            print("ENTERING VERSION CHECKS\n")
            if(rx_version > version): 
                callOtherScripts(otherPi, thisPi)
            elif(otherVersion < thisVersion): 
                callOtherScripts(thisPi, otherPi)
            else: continue
        rx_socket.close()
    
    #Handles the transmission. It loads the transmitting device's IP address into a dictionary and then broadcasts the version number to the network.
    def tx_broadcast(self, version):
        print("TX_BROAD\n")
        return #temp 2 lines to check the flow of the program
        tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.nodeDict.update({tx_socket.gethostbyname(tx_socket.gethostname()): version })
        while True:
            tx_socket.sendto(bytes(str(version), 'utf-8'), (self.BROADCAST_ADDRESS, self.PORT))
        tx_socket.close()



#main of the file
thisPi = Pi(thisVersion, thisAddr)
#while True: #temp commented--------------------------------------------------------
broad = Broadcast()
broad.tx_broadcast(thisVersion)
broad.rx_broadcast()