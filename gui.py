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
        """Runs the Pi-Pi management program and emits all signals."""
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
                ver, addr = bdct.rxBroadcast() # Recieves broadcasts on the network
                ver = int(ver)
                # If program recieves its own broadcast...
                if addr[0] ==  this_Pi.getIP()or addr[0] == "": continue
                else:
                    # If no broadcast found...
                    if ver == int(this_Pi.getVersion()) or ver == -1: continue
                    else:
                        self.status.emit('Truck Found!')
                        time.sleep(1)
                        if ver > int(this_Pi.getVersion()):
                            self.status.emit('Preparing for Update...')
                            self.progress.emit(10)
                            time.sleep(1)
                            # Runs server on this Pi
                            #callOtherScripts(this_Pi, pi.Pi(ver, addr[0]), True)
                        elif ver < this_Pi.getVersion():
                            self.status.emit('Preparing for Transfer...')
                            self.progress.emit(10)
                            time.sleep(1)
                            # Runs client on this Pi
                            #callOtherScripts(this_Pi, pi.Pi(ver, addr[0]), False)
                        break
    
    
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
            self.signalStrength.emit("{} dBm".format(int(getSignal[50:53])))
            self.signalQuality.emit("{:.0%}".format(float(getSignal[30:32])/70.0))

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
        self.technicianButton.clicked.connect(self.technicianMode)
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

    def technicianMode(self):
        """Stops the main worker thread and switches screens to Pi-Phone screen.
            Is called when the technician mode button is pressed.
        """
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.worker.stop(restart = False)

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

class PiPhoneTransfer(QDialog):
    """The class used to design a window with signals and slots for the Pi-Phone
    management program.
    """
    
    def __init__(self):
        super(PiPhoneTransfer, self).__init__()
        loadUi("piphonetransfer.ui",self)

def getSystemIP():
        batcmd = 'hostname -I'
        get_IP = subprocess.check_output(batcmd, shell = True).strip()
        return get_IP.decode("utf-8")

"""The following must be run in both gui.py and main.py:"""
# Creates application screen
app = QApplication(sys.argv)
userScreen = PiPiTransfer()
technicianScreen = PiPhoneTransfer()

# Creates a stackable widget with multiple screens
widget = QtWidgets.QStackedWidget()
widget.addWidget(userScreen)
widget.addWidget(technicianScreen)
widget.setFixedHeight(480)
widget.setFixedWidth(320)
widget.show()

# Runs main event loop thread and exits when "X" is clicked/tapped
sys.exit(app.exec_())