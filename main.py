from tkinter import *
from recording import start_recording, stop_recording

Main_window = Tk()

Main_window.geometry("220x100")

def new_text():
    text.set("this is the new text")


new_text = Button(Main_window, 
			text = "Record",
			command = new_text)

record_btn = Button(Main_window, 
			text = "Record",
			command = start_recording)

stop_btn = Button(Main_window, 
			text = "Stop", 
			command = stop_recording)

text = StringVar()
status = StringVar()

text.set("What should I learn")
status.set("")

status_label = Label(Main_window, 
				textvariable = status)

text_label = Label(Main_window, 
				textvariable = text)


record_btn.pack()
stop_btn.pack()
status_label.pack()
text_label.pack()

Main_window.mainloop()
