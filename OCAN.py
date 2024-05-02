#license GPL-3.0-or-later
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
        try:
            self.conceptFile = open('concepts.json', "r")
            self.conceptData = json.loads(self.conceptFile.read()) 
        except:
            self.errorShow("000000015")
            self.conceptData = {}

        loadUi("OCAN.ui", self)
        self.label.setText(f"Date: {måned} {dato}")
        self.saved = True
        self.savedCE = True
        self.savedN = True
        self.savedNN = True
        self.savedNCon = True
        self.savedCon = True
        self.newNoteSavePushButton = self.findChild(QPushButton,"newNoteSavePushButton")
        self.newNoteTextEdit = self.findChild(QTextEdit, "newNoteTextEdit")
        self.noteEditLayout = self.findChild(QWidget, "noteEditLayout_2")
        self.noteShowLayout = self.findChild(QWidget, "noteShowLayout_2")
        self.noteTextEdit = self.findChild(QTextEdit, "noteTextEdit")
        self.actionCalendar  = self.findChild(QAction, "actionCalendar_2")
        self.actionNew_concept = self.findChild(QAction, "actionNew_concept")
        self.actionNotes  = self.findChild(QAction, "actionNotes")
        self.actionNewNote  = self.findChild(QAction, "actionNew_note")
        self.actionCalendar.triggered.connect(self.exitEditCalendar)
        self.actionNew_concept.triggered.connect(self.newConcept)
        self.calendar = self.findChild(QCalendarWidget,"calendarWidget")
        self.openConceptPageTreeWidget = self.findChild(QTreeWidget,"openConceptPageTreeWidget")
        self.calendarPage = self.findChild(QWidget,"CalendarPage")
        self.openConceptPage = self.findChild(QWidget,"openConceptPage")
        self.conceptPage = self.findChild(QWidget, "conceptPage_2")
        self.notePage = self.findChild(QWidget,"NotePage")
        self.helpPage = self.findChild(QWidget, "helpPage_2")
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
        self.newConceptPage = self.findChild(QWidget, "newConceptPage")
        self.newConceptTitleLineEdit = self.findChild(QLineEdit, "newConceptTitleLineEdit")
        self.newConceptRootPushButton = self.findChild(QPushButton, "newConceptRootPushButton")
        self.newConceptTreeWidget = self.findChild(QTreeWidget, "newConceptTreeWidget")
        self.newConceptTextEdit = self.findChild(QTextEdit, "newConceptTextEdit")
        self.newConceptSavePushButton = self.findChild(QPushButton,"newConceptSavePushButton")
        self.openConceptPathLabel = self.findChild(QLabel, "openConceptPathLabel")
        self.newConceptDescriptionLineEdit = self.findChild(QLineEdit,"newConceptDescriptionLineEdit")
        self.conceptTitelLineEdit = self.findChild(QLineEdit,"conceptTitelLineEdit")
        self.conceptRootShowLabel = self.findChild(QLabel, "conceptRootShowLabel")
        self.conceptDescriptionLineEdit = self.findChild(QLineEdit, "conceptDescriptionLineEdit")
        self.conceptEditLayout = self.findChild(QWidget,"conceptEditLayout")
        self.conceptShowLayout = self.findChild(QWidget, "conceptShowLayout")
        self.conceptTextEdit = self.findChild(QTextEdit,"conceptTextEdit")
        self.conceptSavePushButton = self.findChild(QPushButton,"conceptSavePushButton")
        self.conceptTextBrowser = self.findChild(QTextBrowser, "conceptTextBrowser")
        self.conceptEditPushButton = self.findChild(QPushButton,"conceptEditPushButton")
        self.actionHelp =self.findChild(QAction, "actionHelp")
        self.newNoteTitleLineEdit.textChanged.connect(self.reloadNewNotePath)
        self.newConceptTitleLineEdit.textChanged.connect(self.reloadNewConceptPath)
        self.noteTreeView.itemClicked.connect(self.itemClicked)
        self.openConceptPageTreeWidget.itemClicked.connect(self.conceptItemClicked)
        self.noteTreeView.activated.connect(self.openNote)
        self.eventsComboBox.currentTextChanged.connect(self.updateCalendarEvent)
        self.calendarEventSavePushButton.pressed.connect(self.safeCalendarEvent)
        self.calendarEditSavePushButton.pressed.connect(self.safeCalendar)
        self.calendarNotesTextEdit.textChanged.connect(self.unSave)
        self.calendarEditExitPushButton.pressed.connect(self.exitEditCalendar)
        self.newConceptRootPushButton.pressed.connect(self.changeConceptPath)
        self.newConceptRootPushButton.pressed.connect(self.changeConceptPath)
        self.actionCosepts = self.findChild(QAction,"actionCosepts")
        self.calendarEditPage.hide()
        self.newConceptPage.hide()
        self.noteLoadPage.hide()
        self.notePage.hide()
        self.conceptPage.hide()
        self.newNotePage.hide()
        self.helpPage.hide()
        self.openConceptPage.hide()
        self.label_2 = self.findChild(QLabel,"label_2")
        self.calendar.selectionChanged.connect(self.grab_date)
        self.calendar.activated.connect(self.editCalendar)
        self.actionNotes.triggered.connect(self.openLoadNotes)
        self.actionNewNote.triggered.connect(self.openNewNotes)
        self.noteEditPushButton.pressed.connect(self.editNote)
        self.newNoteTreeWidget.activated.connect(self.showRootLabel)
        self.newConceptTreeWidget.activated.connect(self.showConceptRootLabel)
        self.newNotePathLabel.pressed.connect(self.changePath)
        self.newNoteSavePushButton.pressed.connect(self.saveNewNote)
        self.newConceptSavePushButton.pressed.connect(self.saveNewConcept)
        self.actionCosepts.triggered.connect(self.openConceptTree)
        self.openConceptPageTreeWidget.activated.connect(self.openConcept)
        self.conceptEditPushButton.pressed.connect(self.editConcept)
        self.conceptSavePushButton.pressed.connect(self.saveConcept)
        self.noteSavePushButton = self.findChild(QPushButton, "noteSavePushButton")
        self.noteSavePushButton.pressed.connect(self.saveNote)
        self.noteTextBrowser.anchorClicked.connect(self.linkClicked) 
        self.conceptTextBrowser.anchorClicked.connect(self.linkClicked) 
        self.actionHelp.triggered.connect(self.openHelpPage)

    def openHelpPage(self):
        if self.savedN == False:
            self.safeCheck("N")
        if self.savedNN == False:
            self.safeCheck("NN")
        if self.savedNCon == False:
            self.safeCheck("NC")
        if self.saved == False:
            self.safeCheck("C")
        if self.savedCon == False:
            self.safeCheck("Con")
        self.calendarEditPage.hide()
        self.calendarPage.hide()
        self.newConceptPage.hide()
        self.noteLoadPage.hide()
        self.notePage.hide()
        self.conceptPage.hide()
        self.newNotePage.hide()
        self.helpPage.show()
        self.openConceptPage.hide()
        
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
        if self.savedNCon == False:
            self.safeCheck("NC")
        if self.saved == False:
            self.safeCheck("C")
        if self.savedCon == False:
            self.safeCheck("Con")
        self.newNotePage.hide()
        self.helpPage.hide()
        self.openConceptPage.hide()
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
        self.newConceptPage.hide()
    
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
        if type == "NC":
            dlg.setText("Concept not saved, do you you want to save?")  
        if type == "Con":
            dlg.setText("Concept not saved, do you you want to save?")  
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
            if button == QMessageBox.StandardButton.Yes:
                if self.savedNN == False:
                    self.saveNewNote()
            else:
                self.savedNN = True
        if type == "NCon":
            if button == QMessageBox.StandardButton.Yes:
                if self.savedNCon == False:
                    self.saveNewConcept()
            else:
                self.savedNCon = True
        if type == "Con":
            if button == QMessageBox.StandardButton.Yes:
                if self.savedCon == False:
                    self.saveConcept()
            else:
                self.savedCon = True

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
        if self.savedNCon == False:
            self.safeCheck("NC")
        if self.savedCon == False:
            self.safeCheck("Con")
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
        if self.savedNCon == False:
            self.safeCheck("NC")
        if self.savedCon == False:
            self.safeCheck("Con")
        self.calendarEditPage.hide()
        self.newConceptPage.hide()
        self.noteLoadPage.hide()
        self.notePage.hide()
        self.conceptPage.hide()
        self.newNotePage.hide()
        self.helpPage.hide()
        self.openConceptPage.hide()
        self.calendarPage.show()

    def openLoadNotes(self):
        self.calendarEditPage.hide()
        self.newConceptPage.hide()
        self.noteLoadPage.show()
        self.notePage.hide()
        self.conceptPage.hide()
        self.calendarPage.hide()
        self.newNotePage.hide()
        self.helpPage.hide()
        self.openConceptPage.hide()
        self.loadNoteTree(self.noteFile)
    
    def itemClicked(self):
        item=self.noteTreeView.currentItem()
        text = self.getParentPath(item)
        self.pickedNoteRootLable.setText(text)
        self.currentNote = item.text(0)
        self.currentPath = text      
        
    def conceptItemClicked(self):
        item=self.openConceptPageTreeWidget.currentItem()
        text = self.getParentPath(item)
        self.openConceptPathLabel.setText(text)
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
        self.newConceptPage.hide()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.newNotePage.hide()
        self.helpPage.hide()
        self.openConceptPage.hide()
        self.notePage.show()
        self.conceptPage.hide()
        self.noteShowLayout.show()
        self.noteEditLayout.hide()
        self.noteTextBrowser.clear()
        self.noteTextBrowser.setPlainText("")
        self.noteTextBrowser.setHtml(self.convertNote(self.currentPath))
        self.noteTextBrowser.setOpenExternalLinks(True)
        self.noteTitleLineEdit.setText(self.currentNote)
        self.noteShowRootLabel.setText(self.currentPath)
        self.noteTextBrowser.setToolTip("") 


    def linkClicked(self, url):
        path = url.toString()
        self.currentPath = path
        try: self.openConcept()
        except:self.errorShow("000000020")
    
    def openConcept(self):
        try:
            self.conceptFile = open('concepts.xml', "r").read()
        except:
            self.errorShow("000000014")
        self.calendarEditPage.hide()
        self.newConceptPage.hide()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.newNotePage.hide()
        self.helpPage.hide()
        self.openConceptPage.hide()
        self.notePage.hide()
        self.conceptPage.show()
        self.conceptShowLayout.show()
        self.conceptEditLayout.hide()
        self.conceptTextBrowser.clear()
        self.conceptTextBrowser.setText(self.convertConcept(self.currentPath))
        self.conceptTextBrowser.setOpenExternalLinks(True)
        try:self.conceptDescriptionLineEdit.setText(self.conceptData[self.currentPath][0])
        except:pass
        self.conceptDescriptionLineEdit.setEnabled(False)
        self.conceptTitelLineEdit.setText(self.currentNote)
        self.conceptRootShowLabel.setText(self.currentPath)
        self.noteTextBrowser.setToolTip("") 

    def editConcept(self):
        self.conceptShowLayout.hide()
        self.conceptEditLayout.show()
        self.conceptDescriptionLineEdit.setEnabled(True)
        try: self.conceptTextEdit.setPlainText(self.conceptData[self.currentPath][1])
        except: self.conceptTextEdit.setPlainText("")
        self.savedCon = False


    def saveConcept(self):
        try:
            self.conceptData[self.currentPath] = [self.conceptDescriptionLineEdit.text(),self.conceptTextEdit.toPlainText()]
            conceptFileWrite = open ('concepts.json', "w")
            json.dump(self.conceptData, conceptFileWrite)
            self.savedCon = True
            self.openConcept()
        except:
            self.errorShow("000000019")


    def openConceptTree(self):
        self.calendarEditPage.hide()
        self.newConceptPage.hide()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.newNotePage.hide()
        self.helpPage.hide()
        self.notePage.hide()
        self.conceptPage.hide()
        self.noteShowLayout.hide()
        self.noteEditLayout.hide()
        self.openConceptPage.show()
        try:
            self.conceptFile = open('concepts.xml', "r").read()
        except:
            self.errorShow("000000014")
        if self.saved == False:
            self.safeCheck("C")
        if self.savedN == False:
            self.safeCheck("N")
        if self.savedNN == False:
            self.safeCheck("NN")
        if self.savedNCon == False:
            self.safeCheck("NC")
        if self.savedCon == False:
            self.safeCheck("Con")
        try: 
            tree = et.fromstring(self.conceptFile)
        except:
            root = et.Element("noter")
            tree = et.ElementTree(root)
            with open("notes.xml", "wb") as file:
                tree.write(file)
            tree = et.fromstring(self.noteFile)
        self.openConceptPageTreeWidget.clear()
        self.openConceptPageTreeWidget.setColumnCount(1)
        widgetItem = QTreeWidgetItem([tree.tag])
        self.openConceptPageTreeWidget.addTopLevelItem(widgetItem)
        self.openConceptPageTreeWidget.setHeaderHidden(True)

        def displayNoteTree(widgetItem,s):
            for child in s:
                branch = QTreeWidgetItem([child.attrib["name"]])
                widgetItem.addChild(branch)
                displayNoteTree(branch, child)
            if s.text is not None:
                content = s.text
                widgetItem.addChild(QTreeWidgetItem([content]))
        displayNoteTree(widgetItem, tree)


    def newConcept(self):
        self.calendarEditPage.hide()
        self.newConceptPage.show()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.newNotePage.hide()
        self.helpPage.hide()
        self.notePage.hide()
        self.conceptPage.hide()
        self.openConceptPage.hide()
        self.noteShowLayout.hide()
        self.noteEditLayout.hide()
        self.newConceptRootPushButton.hide()
        self.newConceptTreeWidget.show()
        self.newConceptTitleLineEdit.setText("")
        self.savedNCon =False
        try:
            self.conceptFile = open('concepts.xml', "r").read()
        except:
            self.errorShow("000000014")
        try: 
            tree = et.fromstring(self.conceptFile)
        except:
            root = et.Element("concepts")
            tree = et.ElementTree(root)
            with open("concepts.xml", "wb") as file:
                tree.write(file)
            tree = et.fromstring(self.noteFile)
        self.newConceptTreeWidget.clear()
        self.newConceptTreeWidget.setColumnCount(1)
        widgetItem = QTreeWidgetItem([tree.tag])
        self.newConceptTreeWidget.addTopLevelItem(widgetItem)
        self.newConceptTreeWidget.setHeaderHidden(True)

        def displayNoteTree(widgetItem,s):
            for child in s:
                branch = QTreeWidgetItem([child.attrib["name"]])
                widgetItem.addChild(branch)
                displayNoteTree(branch, child)
            if s.text is not None:
                content = s.text
                widgetItem.addChild(QTreeWidgetItem([content]))
        displayNoteTree(widgetItem, tree)
        
    def changeConceptPath(self):
        self.newConceptTreeWidget.clear()
        self.newConceptRootPushButton.hide()
        self.newConceptTreeWidget.show()
        tree = et.fromstring(self.conceptFile)
        self.newConceptTreeWidget.setColumnCount(1)
        self.newConceptTreeWidget.setHeaderHidden(True)
        widgetItem = QTreeWidgetItem([tree.tag])
        self.newConceptTreeWidget.addTopLevelItem(widgetItem)
        def displayNoteTree(widgetItem,s):
            for child in s:
                branch = QTreeWidgetItem([child.attrib["name"]])
                widgetItem.addChild(branch)
                displayNoteTree(branch, child)
            if s.text is not None:
                content = s.text
                widgetItem.addChild(QTreeWidgetItem([content]))
        displayNoteTree(widgetItem, tree)

    def saveNewConcept(self):
        if not self.savedNCon:
            try:
                itemName = self.newConceptTitleLineEdit.text()
                tree = et.parse("concepts.xml")
                
                tags = self.currentPath.split('/')
                if tags == ["concepts"]:
                    new_current_element = tree.getroot()
                else: 
                    if tags[0] == "concepts":
                        tags.pop(0)
                    current_element = tree

                    for tag in tags:
                        matching_elements = current_element.findall(f'.//Concept[@name="{tag}"]')
                        if matching_elements:
                            new_current_element = matching_elements[0]
                            

                if  f"{self.currentPath}/{itemName}" not in  self.conceptData:
                    et.SubElement(new_current_element, "Concept", name=itemName)
                    tree.write('concepts.xml')
                    
                    try:
                        self.conceptData[f"{self.currentPath}/{itemName}"] = [self.newConceptDescriptionLineEdit.text(), self.newConceptTextEdit.toPlainText()]
                        noteFileWrite = open ('concepts.json', "w")
                        json.dump(self.conceptData, noteFileWrite)
                        self.savedNCon = True
                        self.currentPath = f"{self.currentPath}/{itemName}"
                        self.openConcept()
                    except:
                        self.errorShow("000000017")
                    
                else:
                    self.errorShow("000000016")
                
            except:
                self.errorShow("000000018")
                return

    def showConceptRootLabel(self):
        self.newConceptRootPushButton.show()
        item=self.newConceptTreeWidget.currentItem()
        text = self.getParentPath(item)
        self.newConceptRootPushButton.setText(text)
        self.currentNote = item.text(0)
        self.currentPath = text 
        self.newConceptRootPushButton.setText(f"{self.currentPath}/{self.newConceptTitleLineEdit.text()}")
        self.newConceptTreeWidget.hide()
    
    def reloadNewConceptPath(self):
        try: self.newConceptRootPushButton.setText(f"{self.currentPath}/{self.newConceptTitleLineEdit.text()}")
        except: pass

    def editNote(self):
        self.noteShowLayout.hide()
        self.noteEditLayout.show()
        try: self.noteTextEdit.setPlainText(self.noteData[self.currentPath])
        except: self.noteTextEdit.setPlainText("")
        self.savedN = False
        
        
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
        if self.savedNCon == False:
            self.safeCheck("NC")
        if self.savedCon == False:
            self.safeCheck("Con")
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
        self.newConceptPage.hide()
        self.noteLoadPage.hide()
        self.calendarPage.hide()
        self.notePage.hide()
        self.conceptPage.hide()
        self.newNotePage.show()
        self.helpPage.hide()
        self.openConceptPage.hide()
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
        try:replaced_text = re.sub(pattern, lambda match: "<a title='{0}', href='{1}'>{2}</a>".format(self.conceptData[match.group(1).split("><",1)[0]][0],match.group(1).split("><",1)[0],match.group(1).split("><",1)[1]), text)
        except: replaced_text = text
        prefix = "link["
        suffix = "]"
        pattern = re.escape(prefix) + "(.*?)" + re.escape(suffix)
        try: replaced_text = re.sub(pattern, lambda match: "<a href='{0}'>{1}</a>".format(match.group(1).split(" ",1)[0], match.group(1).split(" ",1)[1]), replaced_text)
        except: pass
        return replaced_text
    
    def convertConcept(self,concept):
        try: text = self.conceptData[concept][1]
        except: text = ""
        prefix = "concept["
        suffix = "]"
        pattern = re.escape(prefix) + "(.*?)" + re.escape(suffix)
        try: replaced_text = re.sub(pattern, lambda match: "<a title='{0}', href='{1}'>{2}</a>".format(self.conceptData[match.group(1).split("><",1)[0]][0],match.group(1).split("><",1)[0],match.group(1).split("><",1)[1]), text)
        except: replaced_text = text
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


