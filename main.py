# importing everything from tkinter
from tkinter import *
from recording import start_recording, stop_recording

# create gui window
Main_window = Tk()

# set the configuration 
# of the window
Main_window.geometry("220x100")

def new_text():
    #potentially add new functions here
    text.set("this is the new text")


# create a Button widget and attached 
# with java function 
new_text = Button(Main_window, 
			text = "Record",
			command = new_text)

# create a Button widget and attached 
# with java function 
record_btn = Button(Main_window, 
			text = "Record",
			command = start_recording)

# create a Button widget and attached 
# with python function
stop_btn = Button(Main_window, 
			text = "Stop", 
			command = stop_recording)

# create a StringVar class
text = StringVar()
status = StringVar()

# set the text
text.set("What should I learn")
status.set("")

# create a label widget
status_label = Label(Main_window, 
				textvariable = status)

# create a label widget
text_label = Label(Main_window, 
				textvariable = text)


# place widgets into 
# the gui window
record_btn.pack()
stop_btn.pack()
status_label.pack()
text_label.pack()

# Start the GUI 
Main_window.mainloop()
