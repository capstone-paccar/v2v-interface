import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget

class PiPiTransfer(QDialog):
    def __init__(self):
        super(PiPiTransfer, self).__init__()
        loadUi("pipitransfer.ui",self) #editor must only open "Pi GUI Folder"
        self.technicianButton.clicked.connect(self.technicianMode)

    def technicianMode(self):
        technicianScreen = PiPhoneTransfer()
        widget.addWidget(technicianScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class PiPhoneTransfer(QDialog):
    def __init__(self):
        super(PiPhoneTransfer, self).__init__()
        loadUi("piphonetransfer.ui",self) #editor must only open "Pi GUI Folder"

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