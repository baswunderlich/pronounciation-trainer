from tkinter import *
from recording import start_recording, stop_recording

# Create the main window
Main_window = Tk()
Main_window.geometry("500x300")
Main_window.title("Audio Recorder")

# Variables for dynamic text updates
text = StringVar()
status = StringVar()

text.set("Read me please!")
status.set("Press 'Record' to start")

# Functions for button actions
def start():
    start_recording()
    status.set("Recording...")

def stop():
    stop_recording()
    status.set("Stopped")

def update_text():
    text.set("This is the new text, wow")

# Buttons for recording, stopping, and updating text
record_btn = Button(Main_window, text="Record", command=start, width=15, height=2, bg="green", fg="white")
stop_btn = Button(Main_window, text="Stop", command=stop, width=15, height=2, bg="red", fg="white")
update_btn = Button(Main_window, text="Update Text", command=update_text, width=15, height=2)

# Labels for displaying dynamic text
status_label = Label(Main_window, textvariable=status, font=("Arial", 12))
text_label = Label(Main_window, textvariable=text, font=("Arial", 12))

# Add widgets to the window
status_label.pack(pady=3)
record_btn.pack(pady=3)
stop_btn.pack(pady=3)
update_btn.pack(pady=3)
text_label.pack(pady=3)

# Run the GUI
Main_window.mainloop()
