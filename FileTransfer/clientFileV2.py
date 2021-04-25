import socket

def Main():
    host = socket.gethostbyname(socket.gethostname())
    port = 5001

    s = socket.socket()
    s.connect((host,port))

    filename = input("Filename? -> ")

    if filename != "q":
        s.send(filename.encode("utf-8"))
        data = s.recv(1024)
        dataStr = data.decode('ascii')
        if dataStr[:6] == "EXISTS":
            filesize = int(dataStr[6:])
            message = input("File Exists, " +str(filesize) + "Bytes, download? (Y/N)? ->")
            if message == "Y" or message =="y":
                sendStr = "OK"
                s.send(sendStr.encode("utf-8"))
                #create new file new_filename and 
                f = open("new_" + filename, "wb")
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                print("Download Complete")
            else:
                print(message +"was not noticed")
                exit()
        else:
            print("File does not exists")#
    s.close()


if __name__ == "__main__":
    Main()




'''
    filename = input("Enter filename you want to transfer> ")
    if(filename != 'q'):
        # client.send(data.encode(FORMAT))
        s.send(filename.encode("utf-8"))
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = (data[6:])
            message = input("File Exists, " + str(filesize)+ "Bytes, download? Y/N >")
            if message == 'Y':
                s.send('OK')
                f = open('new_' + filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize))*100) + "% Done")
                print("Download Complete!")
            else:
                print("File does not exits!")
        s.close()


Main() 
'''