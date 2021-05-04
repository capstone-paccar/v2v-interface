'''
Project: Vehicle to Vehicle Update System (Capstone)
Capstone Team: Aashima Mehta, Cameron Ufland and Austin Gilbert
Last Date of Modification: 05/04/2021
---------------------------------------------------------------------------------------
OUTLINE: THIS IS THE MAIN_SCRIPT/TRUCK_MANAGER_SCRIPT THAT WILL CALL ALL OTHER SCRIPTS

1) detect all trucks around
    2) put all the trucks with their version number into a dictionary
    3) iterate thr the dictionary and check verion #
        4) establish a connection if not established then continue
            i) if version # is less than our version then 
                a) send the ip of our Pi and run the server script on the otherPi
                b) run the client script of our Pi
            ii) else if version # is greater than our version then
                a) run the server on our Pi
                b) run the client on the otherPi
            iii) if versions are same then continue
keep on iterating.
'''

import collections

#dummy variables
thisIP = 'this_IP'
thisVersion = 2

class Pi:
    #getter for the Version
    def getVersion(self):
        return thisVersion

    #getter for the IP addr
    def getIP(self):
        return thisIP

    #try to establish a connection with other PI
    def establishConnection(self, word):
        # send msg
        recieveMsg = None
        if recieveMsg:
            return True
        else:
            return False
    
    #runServer will run the server.py script on pi --> code in "server.py"
    def runServer(self):
        print("Running server ")
    
    #runClient will run the client.py script on pi --> code in "client.py"
    def runClient(self):
        print("Running client ")

#dummy objects
thisPi = Pi()
otherPi = Pi()

#run the scripts according to the call
def callOtherScripts(needUpdate, hasUpdate):
    print("Inside the callOtherScript")
    hasUpdate.runServer()
    needUpdate.runClient()
    return

#detect the trucks around and put them in the dict
'''
Broadcast the versions of the PI and put them in the dict() map
code in "broadcast.py"
'''
thisdict = {'IP1': '1', 'IP2': '2'}


def compareVersions():
    for key in thisdict:
        # try establishing a connection
        if thisPi.establishConnection(key) is True:
            #check version
            if otherPi.getVersion() > thisPi.getVersion():
                callOtherScripts(thisPi, otherPi)
            elif otherPi.getVersion() < thisPi.getVersion():
                callOtherScripts(otherPi, thisPi)
            else:
                continue


#download done MESSAGE
print("FINISHED PROGRAM")

