# TODO: Implement into gui.py program!!

import socket
import pi
import broadcast
import subprocess
import time as time
import time

TIME_INTERVAL =  1.0
PORT = 1750
SIZE =  1024 * 4
FORMAT = "utf-8"
MESSAGE = ""
PROGRESS = 0

def main():
    """Broadcasts the Pi's version number to other Pi's and sets up a server or
    client depending on the version number recieved from other Pis.
    """
    
    # Reads version number of this Pi
    print("Starting...")
    with open('update.txt', 'r') as f:
        version = int(f.readline())
    this_Pi = pi.Pi(version, get_IP_from_sys())
    print(this_Pi.getIP())

    # Loops until Pi is found
    while True:
        # TODO: if 'Cancel' button pressed, exit while loop
        bdct = broadcast.Broadcast(this_Pi.getVersion())
        bdct.txBroadcast() # broadcasts version number to network
        oldTime = time.time()

        # Retries each time interval
        while (time.time()-oldTime) < TIME_INTERVAL:
            print('Searching...')
            ver, addr = bdct.rxBroadcast() # Recieves broadcasts on the network
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
        runServer(local_Pi)
            # Updates this Pi's version if file is successfully transferred
            #local_Pi.setVersion(remote_Pi.getVersion())
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

        with socket.socket() as server: # Starts server
            server.bind(serverAddr)
            server.listen(1) # Listens for remote IP

            server.settimeout(10) # Starts 1 second timer
            conn, connaddr = server.accept()
            print("Connection Successful!")
            with conn:
                filename = conn.recv(SIZE).decode(FORMAT) # Recieves filename
                conn.send("Filename received.".encode(FORMAT))

                #data = conn.recv(SIZE).decode(FORMAT) # Downloads
                chunk = conn.recv(SIZE)
                data = chunk
                while chunk:
                    chunk = conn.recv(SIZE)
                    data = data + chunk
                print("Downloading...")
                with open(filename, 'wb') as update:
                    update.write(data)
                conn.send("File data received.".encode(FORMAT))
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
        with socket.socket() as client: # Starts client
            client.settimeout(10) # Starts 1 second timer
            client.connect(clientAddr)
            print("Connection Successful!")
            client.send('update.txt'.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT) 
            print("[SERVER]: {}".format(msg))
            with open('update.txt', 'rb') as update:
                client.sendfile(update, 0)  
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

