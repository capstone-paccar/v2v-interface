from main import PiPiTransfer
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QWidget

#main
app = QApplication(sys.argv)
start = PiPiTransfer()
widget = QtWidgets.QStackedWidget()
widget.addWidget(start)
widget.setFixedHeight(480)
widget.setFixedWidth(320)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")