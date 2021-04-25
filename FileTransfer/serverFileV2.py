import socket
import threading
import os

def RtrFile(name, sock):
    filenameByte = sock.recv(1024)
    filenameStr = filenameByte.decode('ascii')
    print("FilenameStr",filenameStr)
    if os.path.isfile(filenameStr):
        print("Type:",type(filenameByte))
        print(os.path.getsize(filenameByte))#

        sendStr = "EXISTS" + str(os.path.getsize(filenameByte))

        #Convert the string to byte because otherwise it will not be send
        sock.send((sendStr.encode("utf-8")))
        userResponse = sock.recv(1024)

        #the Responce will be received in byte and will be converted to a string to make it checkable
        userResponceStr = userResponse.decode('ascii')

        if userResponceStr[:2] == 'OK':
            with open(filenameByte, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
        else:
            print("User response not known")
    else:
        sendStr = "ERR"
        sock.send(sendStr.encode("utf-8"))
    sock.close()


def Main():
    host = socket.gethostbyname(socket.gethostname())
    port = 5001

    s = socket.socket()
    s.bind((host,port))
    s.listen(5)

    print("server started.")

    while True:
        c, addr =s.accept()
        print("client connected ip:< " + str(addr) +">")
        t = threading.Thread(target = RtrFile, args=("rtrThread",c))
        t.start()
    s.close()

if __name__ == "__main__":
    Main()


'''
def retrFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        #sock.send("EXISTS " + str(os.path.getsize(filename))
        sendStr = "EXISTS" + str(os.path.getsize(filename))
        sock.send((sendStr.encode("utf-8")))
        userResponse = sock.recv(1024)
        if(userResponse[:2] == 'OK'):
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR")
    sock.close()

def Main():
    host = socket.gethostbyname(socket.gethostname())
    port = 5001

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print("Server Started.")
    while True:
        conn, addr = s.accept()
        print("Client connected ip:<" + str(addr) +">")
        #t = threading.Thread(target=retrFile,args=("retrThread", conn))
        #t.start()
        retrFile("retrThread", conn)
    s.close()

Main()
'''
