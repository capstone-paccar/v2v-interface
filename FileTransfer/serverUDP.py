import socket
import select

host='0.0.0.0'

port=6000
timeout = 3

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(("",port))

print("waiting on port:", port)

while 1:

    data, clientaddr= s.recvfrom(1024)
    if data:
        print("File name: ", data)
        filename = data.strip()
    f = open(filename, "wb")
    
    while True:
        ready = select.select([s], [], [], timeout)
        if ready[0]:
            data, addr = s.recvfrom(1024)
            f.write(data)
        else:
            print("{} Finish!".format(filename))
            f.close()
            break

reply="Got it thanks!"

reply=reply.encode('utf-8')

s.sendto(reply,clientaddr)

clientmsg, clientaddr=s.recvfrom(1024)
