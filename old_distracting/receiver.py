#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  receiver.py
#  Receives a random number and adjust the blinking frequency accordingly 
#  
#  

import socket
from blinking-led import BlinkyLight

blinky = BlinkyLight(26) #create blinky light object
frequency = 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("169.254.122.180", 1240)) #The IP Address needs to be whatever address is sending the frequency
s.setblocking(0) #stops the s.recv from blocking the blinky light program. Needs a try/except to ensure it runs otherwise there is an exception
while True:
	try:
		freq = s.recv(1024).decode("utf-8")
		print(freq)  #test print
		if  int(freq) > 0:
			print("Hi") #test print
			frequency = int(freq)
			
	except:		
		blinky.run(frequency)


