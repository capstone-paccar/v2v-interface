"""Graphical User Interface (GUI)

This file designs a graphical-user-interface which runs all Pi-Pi management
via three threads and four classes.

Notes
-------------------------------------------------------------------------------
Created by Austin Gilbert, Aashima Mehta, and Cameron Ufland for the University
of Washington, Bothell in affiliation with PACCAR Inc.
"""

import sys, time
import socket
import pi
import broadcast
import subprocess
import logging
from PyQt5.uic import loadUi
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QWidget

logging.basicConfig(format="%(message)s", level=logging.INFO)

class MainWorker(QThread):
    """The main worker thread used to run all Pi-Pi management code and update
    status, progress, and version number on the GUI.

        The Pi-Pi management code broadcasts the Pi's version number to other
        Pis and sets up a server or client depending on the version number
        recieved from other Pis.
    
    Attributes
    ----------
    status : pyqtSignal -> str
        the signal to update logging status and display on GUI
    progress : pyqtSignal -> int
        the signal to update the progress bar and display on GUI
    version : pyqtSignal -> int
        the signal to update the version number and display on GUI
    finished : pyqtSignal
        the signal to indicate finishing the thread

    Methods
    -------
    run()
        runs the Pi-Pi management program and emits all signals
    stop()
        stops the thread by setting boolean "running" to false
    """
    
    status = pyqtSignal(str)
    progress = pyqtSignal(int)
    version = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super(MainWorker, self).__init__()
        self.running = True

    def run(self):
        """Runs the Pi-Pi management program and emits all signals. The Pi-Pi
        management program broadcasts the Pi's version number to other Pi's and
        sets up a server or client depending on the version number recieved from
        other Pis.
        """
        
        self.status.emit('Starting...')
        # Reads version number of this Pi
        with open('update.txt', 'r') as file:
            version = int(file.readline())
        self.version.emit(f'{version}')
        this_Pi = pi.Pi(version, getSystemIP())
        time.sleep(1)

        # Loops until Pi is found
        while(self.running):
            # TODO: if 'Cancel' button pressed, exit while loop

            bdct = broadcast.Broadcast(this_Pi.getVersion())
            bdct.txBroadcast() # broadcasts version number to network
            oldTime = time.time()

            # Retries each time interval
            while (time.time()-oldTime) < 1.0:
                self.status.emit('Searching...')
                ver, addr = bdct.rxBroadcast() # Recieves broadcasts on the
                                               # network
                ver = int(ver)

                # If program recieves its own broadcast...
                if addr[0] ==  this_Pi.getIP()or addr[0] == "": continue
                else:
                    # If no broadcast found...
                    if ver == int(this_Pi.getVersion()) or ver == -1: continue
                    else:
                        self.status.emit('Truck Found!')
                        time.sleep(1)
                        
                        # If this Pi has outdated version...
                        if ver > int(this_Pi.getVersion()):
                            self.status.emit('Preparing for Update...')
                            self.progress.emit(10)
                            time.sleep(1)
                            
                            # If server runs on this Pi successfully...
                            if (self.runServer(this_Pi)):
                                this_Pi.setVersion(ver) # Updates this Pi's
                                                        # version number
                        
                        # If this Pi has an up-to-date version...
                        elif ver < this_Pi.getVersion():
                            self.status.emit('Preparing for Transfer...')
                            self.progress.emit(10)
                            time.sleep(1)

                            # Runs client on this Pi
                            self.runClient(pi.Pi(ver, addr[0]))

                        break
    
    def runServer(self, localPi):
        """Runs a TCP server on this Pi, thereby recieving an update file.

        Parameters
        ----------
        localPi : Pi
            the Pi object to designate this Pi
        
        Returns
        -------
        bool
            a boolean representing the success of the function
        """

        # Tries running a TCP server...
        try:
            serverAddr = (localPi.getIP(), 1750) # Creates server address with
                                                 # local IP and Port 1750
            self.status.emit('Establishing Connection...')
            time.sleep(1)

            # Starts server
            with socket.socket() as server:
                server.bind(serverAddr)
                server.listen(1) # Listens for remote client
                server.settimeout(10) # Starts 10 second server timeout timer
                conn, connaddr = server.accept() # Connects to remote client
                self.status.emit('Connection Successful!')
                self.progress.emit(20)
                time.sleep(1)

            # With successful connection...
            with conn:
                self.status.emit('Downloading...')
                self.progress.emit(40)
                time.sleep(1)
                chunk = conn.recv(4096) # Downloads first chunk (4 kB)
                data = chunk # Stores the first chunk

                # While more chunks exist...
                while chunk:
                    chunk = conn.recv(4096) # Downloads chunks
                    data = data + chunk # Stores chunks
                self.progress.emit(90)
                time.sleep(1)

                # Writes stored data to local update file
                with open('update.txt', 'wb') as update:
                    update.write(data)

                self.status.emit("Update Downloaded Successfully!")
                self.progress.emit(100)
                time.sleep(1)
                return True
        
        # Error in running TCP server...
        except:
            self.status.emit("Error: Timeout in server.")
            time.sleep(1)
            return False

    def runClient(self, remotePi):
        """Runs a TCP Client on this Pi, thereby sending an update file.

        Parameters
        ----------
        remotePi : Pi
            the Pi object to designate the remote Pi
        
        Returns
        -------
        bool
            a boolean representing the success of the function
        """

        # Tries running a TCP client...
        try:  
            clientAddr = (remotePi.getIP(), 1750) # Creates client address with
                                                  # local IP and Port 1750
            self.status.emit('Establishing Connection...')
            time.sleep(1)

            # Starts client
            with socket.socket() as client:
                client.settimeout(10) # Starts 10 second client timeout timer
                client.connect(clientAddr) # Connects to remote server
                self.status.emit('Connection Successful!')
                self.progress.emit(20)
                time.sleep(1)

                # Reads and sends stored data to server
                self.status.emit('Sending...')
                self.progress.emit(40)
                time.sleep(1)
                with open('update.txt', 'rb') as update:
                    client.sendfile(update, 0) # Sends file
                self.progress.emit(90)
                time.sleep(1)

                self.status.emit("Update Sent Successfully!")
                self.progress.emit(100)
                time.sleep(1)
                client.close()
                return True
        
        # Error in running TCP server...
        except:
            self.status.emit("Error: Timeout in client.")
            time.sleep(1)
            return False
    
    def stop(self, restart):
        """Stops the thread by setting boolean "running" to false"""
        self.status.emit('Ending Broadcast...')
        time.sleep(1)
        if restart:
            self.status.emit('Restarting...')
            time.sleep(1)
        self.running = False
        self.finished.emit()

class SignalWorker(QThread):
    """The secondary worker thread used to run subprocess terminal commands and
    update the signal strength and signal quality on the GUI.

        The subprocess code uses the "ifconfig" bash command to get information
        on signal strength and quality in the form of a dBm and percentage
        value respectively.

    Attributes
    ----------
    signalStrength : pyqtSignal -> str
        the internal signal to update the signal strength and display on GUI
    signalQuality : pyqtSignal -> str
        the internal signal to update the signal quality and display on GUI

    Methods
    -------
    run()
        runs the subprocess program and emits all signals

    Notes
    -----
    This method will run until the window exits on a click/tap of the "X".
    """
    
    signalStrength = pyqtSignal(str)
    signalQuality = pyqtSignal(str)

    def __init__(self):
        super(SignalWorker, self).__init__()

    def run(self):
        """Runs the subprocess program and emits all signals."""
        while(True):
            batcmd = 'sudo iwlist wlan0 scan | egrep -C 2 "my-mesh-network"'
            getSignal = str(subprocess.check_output(batcmd, shell = True))
            try:
                self.signalStrength.emit('{} dBm'.format(int(getSignal[50:53])))
            except ValueError:
                self.signalStrength.emit('{} dBm'.format(int(getSignal[50:52])))
            except:
                self.signalStrength.emit('Error')
            
            try:
                self.signalQuality.emit('{:.0%}'.format(float(getSignal[30:32])
                                                        /70.0))
            except ValueError:
                self.signalQuality.emit('{:.0%}'.format(float(getSignal[30:31])
                                                        /70.0))
            except:
                self.signalQuality.emit('Error')

class PiPiTransfer(QDialog):
    """The class used to design a window with signals and slots for the Pi-Pi
    management program.

    Methods
    -------
    runProgram()
        manages main worker thread and its signals
    collectSignal()
        manages secondary worker thread and its signals
    technicianMode()
        stops the main worker thread and switches screens to Pi-Phone screen
    cancelled()
        restarts all threads; called when cancel button is pressed
    writeStatus(label)
        writes the status to the GUI
    writeProgress(value)
        writes the progress bar value to the GUI
    writeSignalStrength(label)
        writes the signal strength to the GUI
    writeSignalQuality(label)
        writes the signal quality to the GUI
    writeVersionNum(label)
        writes the version number to the GUI
    """

    def __init__(self):
        super(PiPiTransfer, self).__init__()
        loadUi("pipitransfer.ui",self) #editor must only open "Pi GUI Folder"
        self.cancelButton.clicked.connect(self.cancelled)
        self.runProgram()
        self.collectSignal()
        
    def runProgram(self):
        """Manages main worker thread and its signals."""
        self.worker = MainWorker()
        self.finished.connect(self.worker.deleteLater)
        self.worker.status.connect(self.writeStatus)
        self.worker.version.connect(self.writeVersionNum)
        self.worker.start()

    def collectSignal(self):
        """Manages secondary worker thread and its signals."""
        self.worker2 = SignalWorker()
        self.finished.connect(self.worker2.deleteLater)
        self.worker2.signalStrength.connect(self.writeSignalStrength)
        self.worker2.signalQuality.connect(self.writeSignalQuality)
        self.worker2.start()

    def cancelled(self):
        """Restarts all Threads.
            Is called when the cancel button is pressed.
        """
        self.worker.stop(restart = True)
        self.runProgram()

    def writeStatus(self, label):
        """Writes the status to the GUI.

        Parameters
        ----------
        label : str
            text label to update on the GUI
        """
        self.status.setText(label)
        logging.info(label)

    def writeProgress(self, value):
        """Writes the progress bar value to the GUI.

        Parameters
        ----------
        value : int
            int label to update on the GUI
        """
        self.progressBar.setValue(value)

    def writeSignalStrength(self, label):
        """Writes the signal strength to the GUI.

        Parameters
        ----------
        label : str
            text label to update on the GUI
        """
        self.signalStrength.setText(label)

    def writeSignalQuality(self, label):
        """Writes the signal quality to the GUI.

        Parameters
        ----------
        label : str
            text label to update on the GUI
        """
        self.signalQuality.setText(label)

    def writeVersionNum(self, label):
        """Writes the version number to the GUI.

        Parameters
        ----------
        label : str
            text label to update on the GUI
        """
        self.versionNum.setText(label)

def getSystemIP():
    """Uses a subprocess to get the IP of the local Pi.

    Returns
    -------
    str
        a string representing the IP of the local Pi
    """
    
    batcmd = 'hostname -I'
    getIP = subprocess.check_output(batcmd, shell = True).strip()
    return getIP.decode("utf-8")

"""The following must be run in both gui.py and main.py:"""
# Creates application screen
app = QApplication(sys.argv)
userScreen = PiPiTransfer()

# Creates a stackable widget with multiple screens
widget = QtWidgets.QStackedWidget()
widget.addWidget(userScreen)
widget.setFixedHeight(720)
widget.setFixedWidth(480)
widget.show()

# Runs main event loop thread and exits when "X" is clicked/tapped
sys.exit(app.exec_())
