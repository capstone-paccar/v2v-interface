'''
Project: Vehicle to Vehicle Update System (Capstone)
Capstone Team: Aashima Mehta, Cameron Ufland and Austin Gilbert
Last Date of Modification: 04/30/2021
---------------------------------------------------------------------------------------
OUTLINE: THIS IS THE MAIN_SCRIPT/TRUCK_MANAGER_SCRIPT THAT WILL CALL ALL OTHER SCRIPTS
THIS PROGRAM ALSO USES THREADING ~ Threads are only used here in the program!!!

1) detect all trucks around
2) create threads
    i) call functions in thread according to the version number of truck
    ii) call other threads for other trucks
    iii) assemble all the threads
3) DONE!!!!  ~ print message

'''

import threading
import collections
#create the dictionary function and callOtherScripts function 
#also can add more functions if needed here
'''
dict --> Manually create the dictionary for all the IP addresses mapped to the versions
callOtherScripts(needUpdate, hasUpdate) --> takes two parameters of IP's of pis
    //call the server and client scripts according to the update need
    //create locks in the server/cleint scripts 
    //after the call the update should be done!
    //thread(EXIT) >> IMPORTANT CALL
'''
#dummy variables
thisIP = 'this_IP'
thisVersion = 2

dict1 = {'IP1': '1', 'IP2': '2'}
def callOtherScripts(needUpdate, hasUpdate):
    print("Inside the callOtherScript")


#detect the trucks around and put them in a queue
'''
create a for loop that will go thr the dictionary and the code will try to form a connection with it?
if the connection was successful then we will put the IP address into a queue/array

The way we could do it ---> "ALSO MAKE SURE TO PUT IN A TRY 
for loop to go thr each dic object say "other_pi"
    try{
        set up a connection with the other_pi
        send a message and wait 2 sec before checking the recieved msg
        the other_pi must return with a msg and if we recieve that msg then this pi is around! 
            therefore put this other_pi in the queue/array
    }catch{ 
        if not received a msg then move on
    }
}
'''
queue = []
for addr in dict1:
    try:
        #set up connection?
        queue.append(addr)
    except:
        print()


#create threads according to the number of queue
'''
at this point we know what trucks are around the pi that we are searching for 
therefore create the thread //say 12 is the len of queue
thread[12]
also add locks in the download section of the other files
for loop for all the thread
    if(version of this_truck > other_truck)
        run thread callOtherScripts(other_truck, this_truck) 
    else
        run thread callOtherScripts(this_truck, other,truck)

for loop to wait for all the threads to be done

'''

def worker(arg):
    if arg is None:
        return
    print('\nthread worker function')
    if(thisVersion > para.version())
        callOtherScripts(para, thisIP)
    else if(thisVersion < para.version())
        callOtherScripts(thisIP, para)
    return


threads = []
for i in range(5):
    para = None
    try:    
        para = queue.remove()
    except:
        print()
    t = threading.Thread(target=worker, args =(para,))
    threads.append(t)
    t.start()

for t in threads:
    threads[t].join()


#download done MESSAGE
print("FINISHED DOWNLOAD")

