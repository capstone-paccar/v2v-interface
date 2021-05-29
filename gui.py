"""Graphical User Interface (GUI)

This file designs a graphical-user-interface which runs all Pi-Pi management
via three threads and four classes.

Notes
-------------------------------------------------------------------------------
Created by Austin Gilbert, Aashima Mehta, and Cameron Ufland for the University
of Washington, Bothell in affiliation with PACCAR Inc.
"""

import sys, time
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
    version = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        super(MainWorker, self).__init__()
        self.running = True

    def run(self):
        """Runs the Pi-Pi management program and emits all signals."""
        # TODO: Insert program here
        i = 0
        while(self.running):
            time.sleep(1)
            i += 1
            self.status.emit(f"{i}")
        self.finished.emit()

    def stop(self):
        """Stops the thread by setting boolean "running" to false"""
        self.running = False

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
        i = 100
        while(True):
            time.sleep(1)
            i += 1
            self.signalStrength.emit(f"{i}")
            self.signalQuality.emit(f"{i}")

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
        self.worker.stop()

    def cancelled(self):
        """Restarts all Threads.
            Is called when the cancel button is pressed.
        """
        # TODO: Add cancel functionality
        return

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