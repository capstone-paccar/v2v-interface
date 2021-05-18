
import socket
import pi
import broadcast
import time as time


TIME_INTERVAL =  1.0
PORT = 15201
SIZE =  1024
FORMAT = "utf-8"
version = 5 #needs to be read from file
#======================================================================
#simulate the scripts to run atleast 3 times if failing!
#======================================================================
def main():

     #need to set this up to read it from the file

    this_pi = pi.Pi(version, socket.gethostbyname(socket.gethostname() + '.local'))


    while True:
        print(this_pi.getIP())
        bdct = broadcast.Broadcast(this_pi.getVersion())
        bdct.tx_broadcast()
        oldTime  = time.time()
        while (time.time()-oldTime) < TIME_INTERVAL :
            print(time.time())
            ver, addr = bdct.rx_broadcast()
            print('fluff me')
            ver = int(ver)
            if addr[0] ==  this_pi.getIP()or addr[0] == "":
                print('in  equal address')
                continue
            else:
                if ver == int(this_pi.getVersion()) or ver == -1 :
                    print(this_pi.getIP(), addr)
                    print('in  equal version')
                    continue
                else:
                    if ver > int(this_pi.getVersion()):
                        print('in need update')
                        callOtherScripts(pi.Pi(ver, addr[0]),
                                        this_pi, True)
                    elif ver < this_pi.getVersion():
                        print('in have update')
                        callOtherScripts(this_pi, 
                                        pi.Pi(ver, addr[0]), False)
                    break

#======================================================================
#simulate the scripts to run atleast 3 times if failing!
#======================================================================

def callOtherScripts(hasUpdate, needUpdate, weNeedUpdate):
    if weNeedUpdate:
        if(runServer(needUpdate)):
            #update the Version of the Client assuming update is done by this line!
            needUpdate.setVersion(hasUpdate.getVersion())
    else:
        runClient(hasUpdate)
    return

#======================================================================
#runServer will run the server.py script on pi --> code in "server.py"
#======================================================================
def runServer(needUpdate):
    print("Running server " + needUpdate.getIP())
    print("Server Version : ", needUpdate.getVersion())
    try:

        serverAddr = (needUpdate.getIP(), PORT)
        print("[STARTING] Server is starting.")
        server = socket.socket()
        server.bind(serverAddr)
        server.listen(1)
        print("[LISTENING] Server is listening on IP")

        server.settimeout(10) #10 second timer
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
        print("oh no something died in the server")
        return False

#======================================================================
#runClient will run the client.py script on pi --> code in "client.py"
#======================================================================
def runClient(hasUpdate):
    print("Running client " + hasUpdate.getIP())
    print("server at ", needUpdate.getIP())
    print("Client Version : ", hasUpdate.getVersion())
    try:
        clientAddr = (hasUpdate.getIP(), PORT)
        client = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10) #10 second timer

        client.connect(clientAddr)

        file = open("transfer.txt", "r")
        data = file.read()

        client.send("transfer.txt".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT) 
        print("[SERVER]: {}".format(msg))

        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print("[SERVER]: {}".format(msg))

        file.close()

        client.close()
        return True
    except:
        print("oh no something died in the client")
        return False
