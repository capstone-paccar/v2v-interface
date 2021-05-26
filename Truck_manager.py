"""Truck Manager

This script enables a Raspberry Pi 4 to send files via Ad-Hoc to another Pi
running the same program.

This tool relies on 'version.txt' and 'transfer.txt' text files to log version
information and the file to transfer. Additionally, the tool uses the 'Broadcast'
and 'Pi' objects to better organize the program.

This script requires that 'batman-adv' be installed on the Pi you are running
this program on.
"""

import socket
import os
import pi
import broadcast
import subprocess
import time as time
import time

TIME_INTERVAL =  1.0
PORT = 15201
SIZE =  1024
FORMAT = "utf-8"
MESSAGE = ""
PROGRESS = 0

def main():
    """Broadcasts the Pi's version number to other Pi's and sets up a server or
    client depending on the version number recieved from other Pis.
    """
    
    # Reads version number of this Pi
    print("Starting...")
    with open("update.txt", "r") as file:
        first_line = file.readline()
        try:
            version = int(first_line)
        except:
            version = -1
    this_Pi = pi.Pi(version, get_IP_from_sys())

    # Loops until Pi is found 
    while True:
        # TODO: if 'Cancel' button pressed, exit while loop
        bdct = broadcast.Broadcast(this_Pi.getVersion())
        bdct.tx_broadcast() # broadcasts version number to network
        oldTime  = time.time()

        # Retries each time interval
        while (time.time()-oldTime) < TIME_INTERVAL:
            print('Searching...')
            ver, addr = bdct.rx_broadcast() # Recieves broadcasts on the network
            ver = int(ver)

            # If program recieves its own broadcast...
            if addr[0] ==  this_Pi.getIP()or addr[0] == "": continue
            else:
                # If no broadcast found...
                if ver == int(this_Pi.getVersion()) or ver == -1: continue
                else:
                    print('Truck Found!')
                    if ver > int(this_Pi.getVersion()):
                        print('Preparing for Update...')
                        # Runs server on this Pi
                        callOtherScripts(this_Pi, pi.Pi(ver, addr[0]), True)
                    elif ver < this_Pi.getVersion():
                        print('Preparing for Transfer...')
                        # Runs client on this Pi
                        callOtherScripts(this_Pi, pi.Pi(ver, addr[0]), False)
                    break

def callOtherScripts(local_Pi, remote_Pi, local_need_update):
    """Helper function to direct program to runServer or runClient and simplify
    code.

    Parameters
    ----------
    local_Pi : Pi
        the Pi object to designate this Pi
    remote_Pi : Pi
        the Pi object to designate the remote Pi
    local_need_update : bool
        a boolean which determines the direction of file transfer
    """
    
    if local_need_update:
        # Runs server on this Pi -> recieving update file
        if(runServer(local_Pi)):
            # Updates this Pi's version if file is successfully transferred
            local_Pi.setVersion(remote_Pi.getVersion())
    else:
        # Runs client on this Pi -> sending update file
        runClient(remote_Pi)
    return

def runServer(needUpdate):
    """Runs a TCP Server on this Pi, thereby recieving an update file.

    Parameters
    ----------
    needUpdate : Pi
        the Pi object to designate this Pi
    
    Returns
    -------
    bool
        a boolean representing the success of the function
    """
    
    try:
        serverAddr = (needUpdate.getIP(), PORT)
        print("Establishing Connection...")
        server = socket.socket() # Starts server
        server.bind(serverAddr)
        server.listen(2) # Listens for remote IP

        server.settimeout(1) # Starts 1 second timer
        conn, connaddr = server.accept()
        print("Connection Successful!")
        #recieve the size of the file	
        size = conn.recv(4) #assuming size wont be greater than 1GB	
        print("this is the size " + str(size, "utf-8"))	
        try: 	
            size = int(size) #actual value of the file_size	
        except:	
            size = 100 #dummy value	
        print(size) #-----------------------------PRINTING SIZE AGAIN TO CHECK THE STR TO INT CONVERSION	
        time.sleep(.10) #dummy sleep call to wait before receiveing file information	

        #recieve file info
        filename = conn.recv(SIZE).decode(FORMAT) # Recieves filename
        data = conn.recv(SIZE).decode(FORMAT) # Downloads
        print("Downloading...")

        #adding the while loop
        while data:
            data = conn.recv(1024)
        conn.send("File data received.".encode(FORMAT))

        conn.close() # Disconnects
        print("Update Downloaded Successfully!")
        time.sleep(1) # waits one second to show message
        return True
    except:
        print("Error: Timeout in server.")
        return False

def runClient(hasUpdate):
    """Runs a TCP Client on this Pi, thereby sending an update file.

    Parameters
    ----------
    hasUpdate : Pi
        the Pi object to designate the remote Pi
    
    Returns
    -------
    bool
        a boolean representing the success of the function
    """

    try:
        clientAddr = (hasUpdate.getIP(), PORT)
        print("Establishing Connection...")
        client = socket.socket() # Starts client
        client.settimeout(2) # Starts 2 second timer
        client.connect(clientAddr)
        print("Connection Successful!")

        #send the size of the file in bytes	
        file_size = str(os.path.getsize('update.txt')) + ''	
        client.send(file_size.encode(FORMAT))	
        time.sleep(.10) #dummy sleep for program to proceed in server	
        print("Done sending file-size")	

        #send file
        with open('update.txt', 'rb') as f:
            data = f.read(1024)
            while data:
                client.send(data)
                data = f.read(1024)

        print("Data sent successfully!")

        client.close()
        return True
    except:
        print("Error: Timeout in client.")
        return False

#======================================================================
#rget_IP_from_sys will retrieve the IP from the system
#======================================================================
def get_IP_from_sys():
    batcmd = 'hostname -I'
    get_IP = subprocess.check_output(batcmd, shell = True).strip()
    return get_IP.decode("utf-8")

main()