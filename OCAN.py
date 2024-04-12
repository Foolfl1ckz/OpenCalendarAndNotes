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
except:
    calender = {}

dato = int(date.today().strftime("%d"))
måned = f.getMonth()
color = '#DAE0E6'



""" Dag data:
calender[str("05/04/2024")] = {

"note" : ",

"event" : [""],

"event_description" : {

"": ""
},

"event_time" : {

"": ""
},

"Definitions" : []

}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("OCAN.ui", self)

        self.label.setText(f"Date: {måned} {dato}")

        self.calendar = self.findChild(QCalendarWidget,"calendarWidget")
        self.calendarPage = self.findChild(QWidget,"CalenderPage")
        self.calenderEditPage = self.findChild(QWidget,"CalenderEditPage")
        self.calenderEditPage.hide()
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
        self.pickedDateLabel = self.findChild(QLabel,"PickedDateLabel")
        self.pickedDateLabel.setText(dateSelected)
        self.eventsComboBox = self.findChild(QComboBox,"eventsComboBox")
        self.eventsComboBox.addItem("None selected")
        try: 
            for x in calender[dateSelected]["event"]:
                self.eventsComboBox.addItem(x)
        except:
            pass
        self.eventsComboBox.addItem("New event")
        self.calendarPage.hide()
        self.calenderEditPage.show()
        self.eventsComboBox.currentTextChanged.connect(self.updateCalenderEvent)

    def updateCalenderEvent(self):
        dateSelected = self.calendar.selectedDate()
        dateSelected = str(dateSelected.toString("dd/MM/yyyy"))
        event =  self.eventsComboBox.currentText()
        self.eventTextEdit = self.findChild(QTextEdit,"eventTextEdit")
        self.eventDescriptionTextEdit = self.findChild(QTextEdit,"eventDescriptionTextEdit")
        
        if event != "New event": 
            self.eventTextEdit.setEnabled(False)
            self.eventDescriptionTextEdit.setEnabled(True)
        else: 
            self.eventDescriptionTextEdit.setEnabled(True)
            self.eventTextEdit.setEnabled(True)
            self.eventDescriptionTextEdit.setText("")
        if event != "None selected":
            self.eventTextEdit.setText(event)
        else:
            self.eventTextEdit.setText("")
            self.eventDescriptionTextEdit.setText("")
            self.eventDescriptionTextEdit.setEnabled(False)
        
        
        try:
            self.eventDescriptionTextEdit.setText(calender[dateSelected]["event_description"][event])
        except:
            pass

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


