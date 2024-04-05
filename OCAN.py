import time
import PySimpleGUI as sg #finder et nyt modul
from datetime import date
import json
import funktioner as f

dato = date.today().strftime("%d/%m/%Y")
måned = f.getMonth()
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

"date":  [sg.Text(dato, text_color = "black",background_color=color, font=("Ariel", 15, "bold"))],
"Month":  [sg.Text(måned, text_color = "black",background_color=color, font=("Ariel", 15, "bold"))]
}
def StartProgram():
  layout = [elements["date"],elements["Month"]]
  window = sg.Window(title="OpenCalenderAndNotes", layout=layout,background_color=color).Finalize()
  window.Maximize()
  while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
      break


StartProgram()
