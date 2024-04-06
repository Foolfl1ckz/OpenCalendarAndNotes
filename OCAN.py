import time 
from datetime import date, datetime
import json
import funktioner as f
from PyQt6.QtGui import * #finder et nyt modul, brug "pip install PyQt6" kilde: https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.uic import *

import sys

sys._excepthook = sys.excepthook 
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 
sys.excepthook = exception_hook 



try:
    calenderFile = open ('calender.json', "r")
    calender = json.loads(calenderFile.read())
    print(calender)
except:
    calender = {}

dato = int(date.today().strftime("%d"))
måned = f.getMonth()
color = '#DAE0E6'



""" Dag data:
calender[str("05/04/2024")] = {

"event" : [""],

"event_description" : [""],

"event_time" : [""],

"Definitions" : []

}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("OCAN.ui", self)

        self.label.setText(f"Date: {måned} {dato}")

        self.calendar = self.findChild(QCalendarWidget,"calendarWidget")

        self.label_2 = self.findChild(QLabel,"label_2")
        
        self.calendar.selectionChanged.connect(self.grab_date)
        self.calendar.activated.connect(self.editCalender)


    def grab_date(self):
        dateSelected = self.calendar.selectedDate()
        dateSelected = str(dateSelected.toString("dd/MM/yyyy"))
        try: 
            dateEvent = str(calender[dateSelected]["event"][0])
        except:
            dateEvent = "No events"
        self.label_2.setText(dateEvent)
    
    def editCalender(self):
        dateSelected = self.calendar.selectedDate()
        dateSelected = str(dateSelected.toString("dd/MM/yyyy"))

        print(f"edit calender for date {dateSelected}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


