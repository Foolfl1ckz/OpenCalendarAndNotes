import time 
from datetime import date
import json
import funktioner as f
from PyQt6.QtGui import * #finder et nyt modul, brug "pip install PyQt6" kilde: https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.uic import *

import sys

dato = int(date.today().strftime("%m"))
måned = f.getMonth()
color = '#DAE0E6'

calender = {}


calender[str("05/04/2024")] = {

"event" : [""],

"event_description" : [""],

"event_time" : [""]

}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("OCAN.ui", self)

        self.label.setText(f"Date: {dato}. {måned}")



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


