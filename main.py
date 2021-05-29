"""Main

This script enables a Raspberry Pi 4 to send files via Ad-Hoc to another Pi
running the same program and launches a graphical-user-interface to display
file transfer statistics.

This tool reads and writes from a text file 'update.txt', calls Python files
'truck_manager.py' and 'gui.py', and classes 'Broadcast' and 'Pi'.

This script requires that 'batman-adv' be installed on the Pi you are running
this program on.

Example
-------------------------------------------------------------------------------
To run this program, type the following into the correct directory in terminal:

    $ python3 main.py

Notes
-------------------------------------------------------------------------------
Created by Austin Gilbert, Aashima Mehta, and Cameron Ufland for the University
of Washington, Bothell in affiliation with PACCAR Inc.

Attributes
-------------------------------------------------------------------------------
Vehicle-to-Vehicle Update Delivery System README:
    https://github.com/capstone-paccar/v2v_interface/blob/main/README.md
"""

from gui import PiPiTransfer
from gui import PiPhoneTransfer
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

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