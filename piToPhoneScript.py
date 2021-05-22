import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1

try:
	print("[STARTING PI TO PHONE CONNECTION]")
	server_sock.bind(("",port))
	server_sock.listen(1)
	print("[LISTENING FOR A SERVER CONNECTION]")
	client_sock,address = server_sock.accept()
	client_sock.settimeout(1) 
    #tried adding timeout but not sure if it actually works!
	print("ACCEPTED CONNECTION FROM ",address)

	data = client_sock.recv(1024)
	print("RECIEVED SUCCESSSFULLY [%s]" % data)

	client_sock.close()
	server_sock.close()

except:
	print("Timed out in Pi-to-Phone")

