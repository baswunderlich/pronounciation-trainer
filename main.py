from tkinter import *
from tkinter import ttk
from recording import start_recording, stop_recording
from textgenerator import get_new_text, clean_text
from transcribe import getTranscript
import analyze
import Levenshtein
import difflib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

# Create main window
Main_window = Tk()
Main_window.geometry("800x800")
Main_window.title("Audio Recorder")

# Variables
text_var = StringVar()
status_var = StringVar()
score_var = StringVar()
transcript_var = StringVar()
mode_var = StringVar()
canvas = None

text_var.set("Read me please!")
status_var.set("Press 'Record' to start")
score_var.set("Score: 0.0")
mode_var.set('default')
choices = ['default', 'poetic']

# Functions
def new_text():
    text_var.set(get_new_text(mode_var.get()))

def start():
    start_recording()
    status_var.set("Recording...")

def stop():
    stop_recording()
    transcript = getTranscript()
    transcript_var.set(clean_text(transcript))
    status_var.set("Stopped")
    update_comparison()

def update_comparison():
    original_text = text_var.get()
    user_transcription = transcript_var.get()
    diff, distance, similarity = compare_texts(clean_text(original_text), user_transcription)
    score_var.set(f"Levenshtein Distance: {distance} | Similarity: {similarity:.2f}")
    comparison_text.config(state=NORMAL)
    comparison_text.delete("1.0", END)
    comparison_text.insert(END, "Original Text:\n" + original_text + "\n\n")
    
    print(diff)
    for word in diff:
        if re.match(r'^\?\s*[\+\-]\n$', word):
            continue

        op = word[0]
        text = word[2:]
        
        if op == '-':
            comparison_text.insert(END, text + " ", "error")
        elif op == '+':
            comparison_text.insert(END, text + " ", "addition")
        else:
            comparison_text.insert(END, text + " ", "correct")
    
    comparison_text.config(state=DISABLED)

def compare_texts(original_text, user_transcription):
    distance = Levenshtein.distance(original_text, user_transcription)
    similarity = Levenshtein.ratio(original_text, user_transcription)
    diff = list(difflib.ndiff(original_text.split(), user_transcription.split()))
    return diff, distance, similarity

def show_plot(event):
    """ Automatically show the plot when switching to the Plot tab """
    global canvas
    if notebook.index(notebook.select()) == 1:  # Index 1 is the Plot tab
        wav_file = "output.wav"
        fig = analyze.generate_plot(wav_file)
        if canvas:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=tab2)
        canvas.get_tk_widget().pack(pady=5)
        canvas.draw()

# Notebook Tabs
notebook = ttk.Notebook(Main_window)
tab1 = Frame(notebook)
tab2 = Frame(notebook)
tab3 = Frame(notebook)
notebook.add(tab1, text="Record")
notebook.add(tab2, text="Plot")
notebook.add(tab3, text="Comparison")
notebook.pack(expand=1, fill="both")

notebook.bind("<<NotebookTabChanged>>", show_plot)  # Bind tab switch event

# Tab 1: Recording Controls
Label(tab1, textvariable=status_var, font=("Arial", 12)).pack(pady=5)
Button(tab1, text="Record", command=start, width=15, height=2, bg="green", fg="white").pack(pady=5)
Button(tab1, text="Stop", command=stop, width=15, height=2, bg="red", fg="white").pack(pady=5)
Button(tab1, text="Different Text", command=new_text, width=15, height=2).pack(pady=5)
Label(tab1, textvariable=text_var, font=("Arial", 12), wraplength=800).pack(fill="both",pady=7, padx=10)
OptionMenu(tab1, mode_var, *choices).pack(pady=5)

# Tab 3: Comparison
Label(tab3, textvariable=score_var, font=("Arial", 12)).pack(pady=5)
comparison_text = Text(tab3, wrap=WORD, width=60, height=15, font=("Arial", 12))
comparison_text.pack(padx=10, pady=10)
comparison_text.tag_config("error", foreground="blue", font=("Arial", 12, "italic"))
comparison_text.tag_config("addition", foreground="red", font=("Arial", 12, "bold"))
comparison_text.tag_config("correct", foreground="green", font=("Arial", 12))
comparison_text.config(state=DISABLED)

# Legend
legend_frame = Frame(tab3)
legend_frame.pack(pady=5)
Label(legend_frame, text="Legend:", font=("Arial", 10, "bold")).pack()
Label(legend_frame, text="Green: Correctly said word", fg="green", font=("Arial", 10)).pack()
Label(legend_frame, text="Red: Extra word spoken", fg="red", font=("Arial", 10)).pack()
Label(legend_frame, text="Blue: Expected word missing", fg="blue", font=("Arial", 10)).pack()

new_text()
Main_window.mainloop()
