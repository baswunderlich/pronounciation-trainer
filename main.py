from tkinter import *
from recording import start_recording, stop_recording
from textgenerator import get_new_text
import codecs

Main_window = Tk()

Main_window.geometry("220x100")

def new_text():
    (text, cleaned_text) = get_new_text()
    text_var.set(text)


new_text_btn = Button(Main_window, 
			text = "New Text",
			command = new_text)

record_btn = Button(Main_window, 
			text = "Record",
			command = start_recording)

stop_btn = Button(Main_window, 
			text = "Stop", 
			command = stop_recording)

text_var = StringVar()
status_var = StringVar()

text_var.set("---")
status_var.set("")

status_label = Label(Main_window, 
				textvariable = status_var)

text_label = Label(Main_window, 
				textvariable = text_var)


record_btn.pack()
stop_btn.pack()
new_text_btn.pack()
status_label.pack()
text_label.pack()

Main_window.mainloop()
