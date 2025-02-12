from tkinter import *
from recording import start_recording, stop_recording
import analyze  # Import the function from analyze.py
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
Main_window = Tk()
Main_window.geometry("500x500")
Main_window.title("Audio Recorder")

# Variables for dynamic text updates
text = StringVar()
status = StringVar()
text.set("Read me please!")
status.set("Press 'Record' to start")

# Variables for plot visibility
plot_shown = False
canvas = None  # Placeholder for the plot canvas

# Functions for button actions
def start():
    start_recording()
    status.set("Recording...")

def stop():
    stop_recording()
    status.set("Stopped")

def update_text():
    text.set("This is the new text, wow")

def toggle_plot():
    global plot_shown, canvas
    wav_file = "output.wav"  # Assuming the recorded file is saved as "output.wav"

    if plot_shown:
        # Hide the plot
        canvas.get_tk_widget().pack_forget()
        plot_shown = False
        show_plot_btn.config(text="Show Plots")
    else:
        # Generate plot using analyze.py
        fig = analyze.generate_plot(wav_file)

        # Embed the plot into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=Main_window)
        canvas.get_tk_widget().pack(pady=5)
        canvas.draw()

        plot_shown = True
        show_plot_btn.config(text="Hide Plots")

# Buttons for recording, stopping, updating text, and showing plots
record_btn = Button(Main_window, text="Record", command=start, width=15, height=2, bg="green", fg="white")
stop_btn = Button(Main_window, text="Stop", command=stop, width=15, height=2, bg="red", fg="white")
update_btn = Button(Main_window, text="Update Text", command=update_text, width=15, height=2)
show_plot_btn = Button(Main_window, text="Show Plots", command=toggle_plot, width=15, height=2)

# Labels for displaying dynamic text
status_label = Label(Main_window, textvariable=status, font=("Arial", 12))
text_label = Label(Main_window, textvariable=text, font=("Arial", 12))

# Add widgets to the window
status_label.pack(pady=5)
record_btn.pack(pady=5)
stop_btn.pack(pady=5)
update_btn.pack(pady=5)
show_plot_btn.pack(pady=5)
text_label.pack(pady=5)

# Run the GUI
Main_window.mainloop()
