import time 
from datetime import date, datetime
import json
import funktioner as f
from PyQt6.QtGui import * #brug "pip install PyQt6" kilde: https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.uic import *
import sys
import xml.etree.ElementTree as et
import re

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
        self.savedN = True
        self.savedNN = True
        self.newNoteSavePushButton = self.findChild(QPushButton,"newNoteSavePushButton")
        self.newNoteTextEdit = self.findChild(QTextEdit, "newNoteTextEdit")
        self.noteEditLayout = self.findChild(QWidget, "noteEditLayout_2")
        self.noteShowLayout = self.findChild(QWidget, "noteShowLayout_2")
        self.noteTextEdit = self.findChild(QTextEdit, "noteTextEdit")
        self.actionCalendar  = self.findChild(QAction, "actionCalendar_2")
        self.actionNotes  = self.findChild(QAction, "actionNotes")
        self.actionNewNote  = self.findChild(QAction, "actionNew_note")
        self.actionCalendar.triggered.connect(self.exitEditCalendar)
        self.calendar = self.findChild(QCalendarWidget,"calendarWidget")
        self.calendarPage = self.findChild(QWidget,"CalendarPage")
        self.notePage = self.findChild(QWidget,"NotePage")
        self.newNotePage = self.findChild(QWidget,"newNotePage")
        self.calendarEditPage = self.findChild(QWidget,"CalendarEditPage")
        self.noteLoadPage = self.findChild(QWidget,"NoteLoadPage")
        self.noteEditPushButton = self.findChild(QPushButton, "noteEditPushButton_2")
        self.noteTitleLineEdit = self.findChild(QLineEdit, "noteTitleLineEdit")
        self.noteShowRootLabel = self.findChild(QLabel, "noteShowRootLabel")
        self.noteTextBrowser = self.findChild(QTextBrowser, "noteTextBrowser")
        self.calendarEditExitPushButton = self.findChild(QPushButton, "calendarEditExitPushButton")
        self.calendarNotesTextEdit = self.findChild(QTextEdit,"calendarNotesTextEdit")
        self.pickedDateLabel = self.findChild(QLabel,"PickedDateLabel")
        self.calendarEventSavePushButton = self.findChild(QPushButton,"calendarEventSavePushButton")
        self.calendarEditSavePushButton = self.findChild(QPushButton,"calendarEditSavePushButton")
        self.eventsComboBox = self.findChild(QComboBox,"eventsComboBox")
        self.noteTreeView = self.findChild(QTreeWidget, "noteTreeView")
        self.pickedNoteRootLable = self.findChild(QLabel, "pickedNoteRootLable")
        self.newNotePathLabel = self.findChild(QPushButton, "newNotePathLabel")
        self.newNoteTitleLineEdit = self.findChild(QLineEdit, "newNoteTitleLineEdit")
        self.newNoteTitleLineEdit.textChanged.connect(self.reloadNewNotePath)
        self.noteTreeView.itemClicked.connect(self.itemClicked)
        self.noteTreeView.activated.connect(self.openNote)
        self.eventsComboBox.currentTextChanged.connect(self.updateCalendarEvent)
        self.calendarEventSavePushButton.pressed.connect(self.safeCalendarEvent)
        self.calendarEditSavePushButton.pressed.connect(self.safeCalendar)
        self.calendarNotesTextEdit.textChanged.connect(self.unSave)
        self.calendarEditExitPushButton.pressed.connect(self.exitEditCalendar)
        self.calendarEditPage.hide()
        self.noteLoadPage.hide()
        self.notePage.hide()
        self.newNotePage.hide()
        self.label_2 = self.findChild(QLabel,"label_2")
        self.calendar.selectionChanged.connect(self.grab_date)
        self.calendar.activated.connect(self.editCalendar)
        self.actionNotes.triggered.connect(self.openLoadNotes)
        self.actionNewNote.triggered.connect(self.openNewNotes)
        self.noteEditPushButton.pressed.connect(self.editNote)
        self.newNoteTreeWidget.activated.connect(self.showRootLabel)
        self.newNotePathLabel.pressed.connect(self.changePath)
        self.newNoteSavePushButton.pressed.connect(self.saveNewNote)
        
       
        


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
        if self.savedN == False:
            self.safeCheck("N")
        if self.savedNN == False:
            self.safeCheck("NN")
        if self.saved == False:
            self.safeCheck("C")
        self.newNotePage.hide()
        self.pickedDateLabel.setText(self.dateSelected)
        self.eventsComboBox.clear()
        self.eventsComboBox.addItem("None selected")
        try: 
            for x in calendar[self.dateSelected]["event"]:
                self.eventsComboBox.addItem(x)
            self.calendarNotesTextEdit.setPlainText(calendar[self.dateSelected]["note"])
        except:
            self.errorShow("000000008")
        self.eventsComboBox.addItem("New event")
        self.calendarPage.hide()
        self.calendarEditPage.show()
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
            self.eventDescriptionTextEdit.setPlainText(calendar[self.dateSelected]["event_description"][event])
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
        if type == "N":
            dlg.setText("Note not saved, do you you want to save?")    
        if type == "NN":
            dlg.setText("Note not saved, do you you want to save?")  
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
        if type == "N": 
            if button == QMessageBox.StandardButton.Yes:
                self.saveNote()
            else:
                self.savedN = True
        if type == "NN":
            if self.savedNN == False:
                self.saveNewNote()


    def loadNoteTree(self, s):
        try:
            self.noteFile = open('notes.xml', "r").read()
        except:
            self.errorShow("000000009")
        if self.saved == False:
            self.safeCheck("C")
        if self.savedN == False:
            self.safeCheck("N")
        if self.savedNN == False:
            self.safeCheck("NN")
        try: 
            tree = et.fromstring(self.noteFile)
        except:
            root = et.Element("noter")
            tree = et.ElementTree(root)
            with open("notes.xml", "wb") as file:
                tree.write(file)
            tree = et.fromstring(self.noteFile)
        self.noteTreeView.clear()
        self.noteTreeView.setColumnCount(1)
        widgetItem = QTreeWidgetItem([tree.tag])
        self.noteTreeView.addTopLevelItem(widgetItem)
        self.noteTreeView.setHeaderHidden(True)

        def displayNoteTree(widgetItem,s):
            for child in s:
                branch = QTreeWidgetItem([child.attrib["name"]])
                widgetItem.addChild(branch)
                displayNoteTree(branch, child)
            if s.text is not None:
                content = s.text
                widgetItem.addChild(QTreeWidgetItem([content]))
        displayNoteTree(widgetItem, tree)

    def exitEditCalendar(self):
        if self.saved == False:
         self.safeCheck("C")
        if self.savedN == False:
         self.safeCheck("N")
        if self.savedNN == False:
            self.safeCheck("NN")
        self.calendarEditPage.hide()
        self.noteLoadPage.hide()
        self.notePage.hide()
        self.newNotePage.hide()
        self.calendarPage.show()

    def openLoadNotes(self):
        self.calendarEditPage.hide()
        self.noteLoadPage.show()
        self.notePage.hide()
        self.calendarPage.hide()
        self.newNotePage.hide()
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
        try:
            self.noteFile = open('notes.xml', "r").read()
        except:
            self.errorShow("000000009")
        self.calendarEditPage.hide()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.newNotePage.hide()
        self.notePage.show()
        self.noteShowLayout.show()
        self.noteEditLayout.hide()
        self.noteTextBrowser.setText(self.convertNote(self.currentPath))
        self.noteTextBrowser.setOpenExternalLinks(True)
        self.noteTextBrowser.anchorClicked.connect(self.linkClicked) 
        self.noteTitleLineEdit.setText(self.currentNote)
        self.noteShowRootLabel.setText(self.currentPath)
    
    def linkClicked(self, url):
        print("Link clicked:", url.toString())

    def editNote(self):
        self.noteShowLayout.hide()
        self.noteEditLayout.show()
        self.noteTextEdit.setPlainText(self.noteData[self.currentPath])
        try: self.noteTextEdit.setPlainText(self.noteData[self.currentPath])
        except: self.noteTextEdit.setPlainText("")
        self.savedN = False
        self.noteSavePushButton = self.findChild(QPushButton, "noteSavePushButton")
        self.noteSavePushButton.pressed.connect(self.saveNote)
        

    def saveNote(self):
        try:
            self.noteData[self.currentPath] = self.noteTextEdit.toPlainText()
            noteFileWrite = open ('data.json', "w")
            json.dump(self.noteData, noteFileWrite)
            self.savedN = True
            self.openNote()
        except:
            self.errorShow("000000011")


    def openNewNotes(self):

        if self.saved == False:
            self.safeCheck("C")
        if self.savedN == False:
            self.safeCheck("N")
        if self.savedNN == False:
            self.safeCheck("NN")
        try:
            self.noteFile = open('notes.xml', "r").read()
        except:
            self.errorShow("000000009")
        self.savedNN = False 
        self.newNoteTreeWidget.clear()
        self.newNoteTreeWidget.show()
        self.newNotePathLabel.hide()
        self.newNotePathLabel.setText("")
        self.newNoteTitleLineEdit.clear()
        try: 
            tree = et.fromstring(self.noteFile)
        except:
            root = et.Element("noter")
            tree = et.ElementTree(root)
            with open("notes.xml", "wb") as file:
                tree.write(file)
            tree = et.fromstring(self.noteFile)
            
        self.calendarEditPage.hide()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.notePage.hide()
        self.newNotePage.show()
        self.newNoteTreeWidget = self.findChild(QTreeWidget, "newNoteTreeWidget")
        self.newNoteTreeWidget.setColumnCount(1)
        self.newNoteTreeWidget.setHeaderHidden(True)
        widgetItem = QTreeWidgetItem([tree.tag])
        self.newNoteTreeWidget.addTopLevelItem(widgetItem)
        
        

        def displayNoteTree(widgetItem,s):
            for child in s:
                branch = QTreeWidgetItem([child.attrib["name"]])
                widgetItem.addChild(branch)
                displayNoteTree(branch, child)
            if s.text is not None:
                content = s.text
                widgetItem.addChild(QTreeWidgetItem([content]))
        displayNoteTree(widgetItem, tree)

    def saveNewNote(self):
        if not self.savedNN:
            try:
                itemName = self.newNoteTitleLineEdit.text()
                tree = et.parse("notes.xml")
                
                tags = self.currentPath.split('/')
                if tags == ["noter"]:
                    new_current_element = tree.getroot()
                else: 
                    if tags[0] == "noter":
                        tags.pop(0)
                    current_element = tree

                    for tag in tags:
                        matching_elements = current_element.findall(f'.//Note[@name="{tag}"]')
                        if matching_elements:
                            new_current_element = matching_elements[0]
                            

                if  f"{self.currentPath}/{itemName}" not in self.noteData:
                    et.SubElement(new_current_element, "Note", name=itemName)
                    tree.write('notes.xml')
                    
                    try:
                        self.noteData[f"{self.currentPath}/{itemName}"] = self.newNoteTextEdit.toPlainText()
                        noteFileWrite = open ('data.json', "w")
                        json.dump(self.noteData, noteFileWrite)
                        self.savedNN = True
                        self.currentPath = f"{self.currentPath}/{itemName}"
                        self.openNote()
                    except:
                        self.errorShow("000000011")
                    
                else:
                    self.errorShow("000000013")
                
            except:
                self.errorShow("000000012")
                return

    def showRootLabel(self):
        self.newNotePathLabel.show()
        item=self.newNoteTreeWidget.currentItem()
        text = self.getParentPath(item)
        self.pickedNoteRootLable.setText(text)
        self.currentNote = item.text(0)
        self.currentPath = text 
        self.newNotePathLabel.setText(f"{self.currentPath}/{self.newNoteTitleLineEdit.text()}")
        self.newNoteTreeWidget.hide()
        

    def convertNote(self,note):
        try: text = self.noteData[note]
        except: text = ""
        prefix = "concept["
        suffix = "]"
        pattern = re.escape(prefix) + "(.*?)" + re.escape(suffix)
        replaced_text = re.sub(pattern, lambda match: "<a href='{0}'>{2}</a>".format(match.group(1),match.group(1)), text)
        prefix = "link["
        suffix = "]"
        pattern = re.escape(prefix) + "(.*?)" + re.escape(suffix)
        try: replaced_text = re.sub(pattern, lambda match: "<a href='{0}'>{1}</a>".format(match.group(1).split(" ",1)[0], match.group(1).split(" ",1)[1]), replaced_text)
        except: pass
        return replaced_text

    def changePath(self):
        self.newNoteTreeWidget.clear()
        self.newNotePathLabel.hide()
        self.newNoteTreeWidget.show()
        tree = et.fromstring(self.noteFile)
        self.newNoteTreeWidget = self.findChild(QTreeWidget, "newNoteTreeWidget")
        self.newNoteTreeWidget.setColumnCount(1)
        self.newNoteTreeWidget.setHeaderHidden(True)
        widgetItem = QTreeWidgetItem([tree.tag])
        self.newNoteTreeWidget.addTopLevelItem(widgetItem)
        def displayNoteTree(widgetItem,s):
            for child in s:
                branch = QTreeWidgetItem([child.attrib["name"]])
                widgetItem.addChild(branch)
                displayNoteTree(branch, child)
            if s.text is not None:
                content = s.text
                widgetItem.addChild(QTreeWidgetItem([content]))
        displayNoteTree(widgetItem, tree)
        

    def reloadNewNotePath(self):
        try: self.newNotePathLabel.setText(f"{self.currentPath}/{self.newNoteTitleLineEdit.text()}")
        except: pass

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


