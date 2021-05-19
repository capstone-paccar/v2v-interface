import socket
import pi
import broadcast
import os
import subprocess
import time as time


TIME_INTERVAL =  1.0
PORT = 15201
SIZE =  1024
FORMAT = "utf-8"
version = 0 #needs to be read from file
#======================================================================
#simulate the scripts to run atleast 3 times if failing!
#======================================================================
def main():

     #need to set this up to read it from the file
    print("in Main")
    f = open("version.txt", "r")
    version = int(f.read())
    f.close()
    this_pi = pi.Pi(version, get_IP_from_sys())


    while True:
        print('this Pi:', this_pi.getIP())
        print('this Pi version:', this_pi.getVersion() )
        bdct = broadcast.Broadcast(this_pi.getVersion())
        bdct.tx_broadcast()
        oldTime  = time.time()
        while (time.time()-oldTime) < TIME_INTERVAL :
            print(time.time())
            ver, addr = bdct.rx_broadcast()
            print('after broadcast')
            ver = int(ver)
            print('remote Pi:', addr[0])
            print('remote Pi version:', ver)
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
                        callOtherScripts(this_pi, 
                                        pi.Pi(ver, addr[0]), True)
                    elif ver < this_pi.getVersion():
                        print('in have update')
                        callOtherScripts(this_pi, 
                                        pi.Pi(ver, addr[0]), False)
                    break

#======================================================================
#helper function to keep the code nice and clean
#======================================================================

def callOtherScripts(local_Pi, remote_Pi, local_need_update):
    if local_need_update:
        if(runServer(local_Pi)):
            #update the Version of the Client assuming update is done by this line!
            local_pi.setVersion(remote_Pi.getVersion())
    else:
        runClient(remote_Pi)
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
    print("server at ", hasUpdate.getIP())
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
#======================================================================
#rget_IP_from_sys will retrieve the IP from the system
#======================================================================
def get_IP_from_sys():
    batcmd = 'hostname -I'
    get_IP = str(subprocess.check_output(batcmd, shell = True))
    get_IP = get_IP[0:len(get_IP)-2]
    return get_IP