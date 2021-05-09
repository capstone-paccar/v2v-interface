import socket
import pi
import broadcast
import threading
import time

PORT = 15200
SIZE = 1024
FORMAT = "utf-8"

#======================================================================
#simulate the scripts to run atleast 3 times if failing!
#======================================================================
def runProgram():
    print("We are in Main")
    version  = 1 #need to set this up to read it from the file
    this_pi = pi.Pi(version, 
                 socket.gethostbyname(socket.gethostname()))
    bdct = broadcast.Broadcast(version, 15200, '255.255.255.255')

    while True:
        print("Inside the main loop")
        bdct.tx_broadcast()
        ver, addr = bdct.rx_broadcast()
        ver = int(ver)
        print(ver)
        print(addr)
        if addr[0] == None or addr[0] == this_pi.getIP():
            print("in addr continue")
            continue
        else:
            if ver == None or ver == this_pi.getVersion():
                print("in version continue")
                continue
            else:
                if ver > this_pi.getVersion():
                    print("Our pi has lesser ver --> run server")
                    callOtherScripts(pi.Pi(ver, addr),
                                     this_pi, True)
                elif ver < this_pi.getVersion():
                    print("Our pi has greater version --> run client")
                    callOtherScripts(this_pi, 
                                     pi.Pi(ver, addr), False)
        print("Done with transfer")

#============================================================================
#callOtherScripts will run sender and reciever scripts according to version
# hasUpdate - contains the info of which pi has the update
# needUpdate - contains the info of which pi needs the update
# Boolean weNeedUpdate - tells if it is our pi that needs the update
#============================================================================
def callOtherScripts(hasUpdate, needUpdate, weNeedUpdate):
    times = 0 
    print("Inside the callOtherScript")
    while(times < 3):
        if weNeedUpdate:
            if(runServer(hasUpdate)):
                #update the Version of the Client
                needUpdate.setVersion(hasUpdate.getVersion())
                print("Client Version : " + str(needUpdate.getVersion()))
                break
        else:
            if(runClient(needUpdate)):
                break
        times = times + 1
    return

#======================================================================
#runServer will run the server.py script on pi --> code in "server.py"
#======================================================================
def runServer(needUpdate):
    print("Running server " + str(needUpdate.getIP()))
    print("Server Version : " + str(needUpdate.getVersion()))
    try:
        serverAddr = ('0.0.0.0', PORT)
        print("[STARTING] Server is starting.")
        server = socket.socket() #(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(serverAddr)
        server.listen(1)
        print("[LISTENING] Server is listening.")

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

#======================================================================
#runClient will run the client.py script on pi --> code in "client.py"
#======================================================================
def runClient(hasUpdate):
    print("Running client " + str(hasUpdate.getIP()))
    print("Client Version : " + str(hasUpdate.getVersion()))
    try:
        clientAddr = (hasUpdate.getIP(), PORT)
        client = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)

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
        return False

def broadcastTheIP(version):
    while True:
        print("BROAD")
        time.sleep(2)
        bdct = broadcast.Broadcast(version, 15200, '255.255.255.255')
        bdct.tx_broadcast()

def main():
    x = threading.Thread(target=broadcastTheIP, args=(1,))
    x.start()
    y = threading.Thread(target=runProgram, args=())
    y.start()
    x.join()
    y.join()

main()
