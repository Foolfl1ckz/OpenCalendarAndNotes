import time
import PySimpleGUI as sg
from datetime import date
import json

dato = date.today().strftime("%d/%m/%Y")
color = '#DAE0E6'

calender = {}


calender[str("05/04/2024")] = {
"day": 5,

"month" : 4,

"year" : 2024,

"weekday" : "Friday",

"event" : [""],

"event_description" : [""],

"event_time" : [""]

}


print(calender) 
elements = {

"date":  [sg.Text(dato, text_color = "black",background_color=color, font=("Ariel", 15, "bold"))]

}
def StartProgram():
  layout = [elements["date"]]
  window = sg.Window(title="OpenCalenderAndNotes", layout=layout,background_color=color).Finalize()
  window.Maximize()
  while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
      break


StartProgram()
