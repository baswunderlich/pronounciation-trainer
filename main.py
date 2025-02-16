from tkinter import *
from tkinter import ttk
from recording import start_recording, stop_recording
from textgenerator import get_new_text, clean_text
from transcribe import getTranscript
import analyze
import Levenshtein
import difflib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
plot_shown = False
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

def toggle_plot():
    global plot_shown, canvas
    wav_file = "output.wav"
    if plot_shown:
        canvas.get_tk_widget().pack_forget()
        plot_shown = False
        show_plot_btn.config(text="Show Plots")
    else:
        fig = analyze.generate_plot(wav_file)
        canvas = FigureCanvasTkAgg(fig, master=tab2)
        canvas.get_tk_widget().pack(pady=5)
        canvas.draw()
        plot_shown = True
        show_plot_btn.config(text="Hide Plots")

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
        if word.startswith('-'):
            comparison_text.insert(END, word[2:] + " ", "error")
        elif word.startswith('+'):
            comparison_text.insert(END, word[2:] + " ", "addition")
        else:
            comparison_text.insert(END, word[2:] + " ", "correct")
    comparison_text.config(state=DISABLED)

def compare_texts(original_text, user_transcription):
    distance = Levenshtein.distance(original_text, user_transcription)
    similarity = Levenshtein.ratio(original_text, user_transcription)
    diff = list(difflib.ndiff(original_text.split(), user_transcription.split()))
    return diff, distance, similarity

# Notebook Tabs
notebook = ttk.Notebook(Main_window)
tab1 = Frame(notebook)
tab2 = Frame(notebook)
tab3 = Frame(notebook)
notebook.add(tab1, text="Record")
notebook.add(tab2, text="Plot")
notebook.add(tab3, text="Comparison")
notebook.pack(expand=1, fill="both")

# Tab 1: Recording Controls
Label(tab1, textvariable=status_var, font=("Arial", 12)).pack(pady=5)
Button(tab1, text="Record", command=start, width=15, height=2, bg="green", fg="white").pack(pady=5)
Button(tab1, text="Stop", command=stop, width=15, height=2, bg="red", fg="white").pack(pady=5)
Button(tab1, text="Update Text", command=new_text, width=15, height=2).pack(pady=5)
Label(tab1, textvariable=text_var, font=("Arial", 12), wraplength=700).pack(fill="both", expand=True, padx=10)
OptionMenu(tab1, mode_var, *choices).pack(pady=5)

# Tab 2: Plot
show_plot_btn = Button(tab2, text="Show Plots", command=toggle_plot, width=15, height=2)
show_plot_btn.pack(pady=5)

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
Label(legend_frame, text="Red: Wrong said word", fg="red", font=("Arial", 10)).pack()
Label(legend_frame, text="Blue: Actual correct word", fg="blue", font=("Arial", 10)).pack()

new_text()
Main_window.mainloop()
