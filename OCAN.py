import time 
from datetime import date, datetime
import json
import funktioner as f
from PyQt6.QtGui import * #finder et nyt modul, brug "pip install PyQt6" kilde: https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.uic import *
import sys
import xml.etree.ElementTree as et

sys._excepthook = sys.excepthook 
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 
sys.excepthook = exception_hook 



try:
    calendarFile = open ('calendar.json', "r")
    calendar = json.loads(calendarFile.read())
except:
    calendar = {}


dato = int(date.today().strftime("%d"))
måned = f.getMonth()
color = '#DAE0E6'



""" Dag data:
calendar[str("05/04/2024")] = {

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
        try:
            errorFile = open ('Errors.json', "r")
            self.errors = json.loads(errorFile.read())
        except:
            self.errorShow("000000001", "Error messages could not load")
        try:
            self.noteFile = open('notes.xml', "r").read()
        except:
            self.errorShow("000000009")
        try:
            self.dataFile = open('data.json', "r")
            self.noteData = json.loads(self.dataFile.read())
        except:
            self.errorShow("000000010")
            self.noteData = {}

        loadUi("OCAN.ui", self)
        self.label.setText(f"Date: {måned} {dato}")
        self.saved = True
        self.savedCE = True
        self.actionCalendar  = self.findChild(QAction, "actionCalendar_2")
        self.actionNotes  = self.findChild(QAction, "actionNotes")
        self.actionCalendar.triggered.connect(self.exitEditCalendar)
        self.calendar = self.findChild(QCalendarWidget,"calendarWidget")
        self.calendarPage = self.findChild(QWidget,"CalendarPage")
        self.notePage = self.findChild(QWidget,"NotePage")
        self.calendarEditPage = self.findChild(QWidget,"CalendarEditPage")
        self.noteLoadPage = self.findChild(QWidget,"NoteLoadPage")
        self.calendarEditPage.hide()
        self.noteLoadPage.hide()
        self.notePage.hide()
        self.label_2 = self.findChild(QLabel,"label_2")
        self.calendar.selectionChanged.connect(self.grab_date)
        self.calendar.activated.connect(self.editCalendar)
        self.actionNotes.triggered.connect(self.openLoadNotes)
        
        


    def grab_date(self):
        self.dateSelected = self.calendar.selectedDate()
        self.dateSelected = str(self.dateSelected.toString("dd/MM/yyyy"))
        try: 
            if self.dateSelected not in calendar:
                calendar[self.dateSelected] = {
                    "note" : "",
                    "event" : [],
                    "event_description" : {}
                                             }
            else:

                if "event_description" not in calendar[self.dateSelected]:
                        calendar[self.dateSelected]["event_description"]={}
                if "note" not in calendar[self.dateSelected]:
                        calendar[self.dateSelected]["note"] = {}
        except:
                self.errorShow("000000004")
        try: 
            dateEvent = str(calendar[self.dateSelected]["event"][0])
        except:
            dateEvent = "No events"
        self.label_2.setText(dateEvent)
    
    def editCalendar(self):
        self.calendarEditExitPushButton = self.findChild(QPushButton, "calendarEditExitPushButton")
        self.calendarNotesTextEdit = self.findChild(QTextEdit,"calendarNotesTextEdit")
        self.pickedDateLabel = self.findChild(QLabel,"PickedDateLabel")
        self.pickedDateLabel.setText(self.dateSelected)
        self.eventsComboBox = self.findChild(QComboBox,"eventsComboBox")
        self.eventsComboBox.clear()
        self.eventsComboBox.addItem("None selected")
        self.calendarEventSavePushButton = self.findChild(QPushButton,"calendarEventSavePushButton")
        self.calendarEditSavePushButton = self.findChild(QPushButton,"calendarEditSavePushButton")
        self.calendarEditExitPushButton.pressed.connect(self.exitEditCalendar)
        try: 
            for x in calendar[self.dateSelected]["event"]:
                self.eventsComboBox.addItem(x)
            self.calendarNotesTextEdit.setText(calendar[self.dateSelected]["note"])
        except:
            self.errorShow("000000008")
        self.calendarNotesTextEdit.textChanged.connect(self.unSave)
        self.eventsComboBox.addItem("New event")
        self.calendarPage.hide()
        self.calendarEditPage.show()
        self.eventsComboBox.currentTextChanged.connect(self.updateCalendarEvent)
        self.calendarEventSavePushButton.pressed.connect(self.safeCalendarEvent)
        self.calendarEditSavePushButton.pressed.connect(self.safeCalendar)
    def unSave(self):
        self.saved = False

    def updateCalendarEvent(self):

        self.savedCE = False
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
            self.eventDescriptionTextEdit.setText(calendar[self.dateSelected]["event_description"][event])
        except:
            #self.errorShow("000000003")
            pass
    
    def safeCalendarEvent(self):
        try: 
            if self.eventTextEdit.toPlainText() != "New event" and self.eventTextEdit.toPlainText() != "" and self.eventTextEdit.toPlainText() != "None selected" and self.eventsComboBox.findText(self.eventTextEdit.toPlainText()) == -1:
                if self.eventTextEdit.toPlainText() not in calendar[self.dateSelected]["event"]: calendar[self.dateSelected]["event"].append(self.eventTextEdit.toPlainText())
                calendar[self.dateSelected]["event_description"][self.eventTextEdit.toPlainText()] = self.eventDescriptionTextEdit.toPlainText()
                
                self.eventsComboBox.insertItem(self.eventsComboBox.currentIndex(),self.eventTextEdit.toPlainText())
                self.savedCE = True
                self.saved = False
            else:
                self.savedCE = True
        except:
            self.errorShow("000000005")

    def safeCalendar(self):

        if self.savedCE == False:
            self.safeCheck("CE")
        try:
            if self.saved == False: 
                calendar[self.dateSelected]["note"] = self.calendarNotesTextEdit.toPlainText()
                try:
                    calendarFileWrite = open ('calendar.json', "w")
                    json.dump(calendar, calendarFileWrite)
                    self.saved = True
                except:
                    self.errorShow("000000007")
        except:
            self.errorShow("000000006")
            



    def safeCheck(self, type):
        global calendar
        dlg = QMessageBox(self)
        dlg.setWindowTitle("You haven't saved!")
        if type == "CE":
            dlg.setText("Event not saved, do you you want to save?")
        if type == "C":
            dlg.setText("Calender not saved, do you you want to save?")    
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if type == "CE":
            if button == QMessageBox.StandardButton.Yes:
                self.safeCalendarEvent()      
            elif self.saved == False: 
                self.safeCalendar(self)
        if type == "C":
            if button == QMessageBox.StandardButton.Yes:
                self.safeCalendar()
            else:
                self.saved = True
                try:
                    calendarFile = open ('calendar.json', "r")
                    calendar = json.loads(calendarFile.read())
                except:
                    calendar = {}
    
    def loadNoteTree(self, s):
        tree = et.fromstring(s)
        self.noteTreeView = self.findChild(QTreeWidget, "noteTreeView")
        self.pickedNoteRootLable = self.findChild(QLabel, "pickedNoteRootLable")
        self.noteTreeView.clear()
        self.noteTreeView.setColumnCount(1)
        widgetItem = QTreeWidgetItem([tree.tag])
        self.noteTreeView.addTopLevelItem(widgetItem)
        self.noteTreeView.itemClicked.connect(self.itemClicked)
        self.noteTreeView.activated.connect(self.openNote)
        self.noteTreeView.setHeaderHidden(True)

        def displayNoteTree(widgetItem,s):
            for child in s:
                branch = QTreeWidgetItem([child.tag])
                widgetItem.addChild(branch)
                displayNoteTree(branch, child)
            if s.text is not None:
                content = s.text
                widgetItem.addChild(QTreeWidgetItem([content]))
        displayNoteTree(widgetItem, tree)

    def exitEditCalendar(self):
        if self.saved == False:
         self.safeCheck("C")
        self.calendarEditPage.hide()
        self.noteLoadPage.hide()
        self.notePage.hide()
        self.calendarPage.show()

    def openLoadNotes(self):
        self.calendarEditPage.hide()
        self.noteLoadPage.show()
        self.notePage.hide()
        self.calendarPage.hide()
        self.loadNoteTree(self.noteFile)
    
    def itemClicked(self):
        item=self.noteTreeView.currentItem()
        text = self.getParentPath(item)
        self.pickedNoteRootLable.setText(text)
        self.currentNote = item.text(0)
        self.currentPath = text      
    
    def getParentPath(self, item):
        def getParent(item,outstring):
            if item.parent() is not None:
                outstring = item.parent().text(0) + "/"+outstring
                return getParent(item.parent(),outstring)
            else:
                return outstring
        return getParent(item,item.text(0))

    def openNote(self):
        self.calendarEditPage.hide()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.notePage.show()
        self.noteEditLayout = self.findChild(QWidget, "noteEditLayout_2")
        self.noteEditLayout.hide()
        self.noteTitleLineEdit = self.findChild(QLineEdit, "noteTitleLineEdit")
        self.noteShowRootLabel = self.findChild(QLabel, "noteShowRootLabel")
        self.noteTitleLineEdit.setText(self.currentNote)
        self.noteShowRootLabel.setText(self.currentPath)

        


    def errorShow(self, errorNumber, errorMessage=""):
        
        try: 
            if errorMessage == "":
                errorMessage = self.errors[errorNumber]
        except:
            olderrorNumber = errorNumber[:]
            errorNumber = "000000002"
            errorMessage = f"Error with no error message: {olderrorNumber}"
        button = QMessageBox.critical(
            self,
            f"Error: {errorNumber}",
            f"Message: {errorMessage}",
            buttons=QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Close,
            defaultButton=QMessageBox.StandardButton.Discard,
        )

        if button == QMessageBox.StandardButton.Discard:
            pass
        elif button == QMessageBox.StandardButton.Close:
            pass
        else:
            pass


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


