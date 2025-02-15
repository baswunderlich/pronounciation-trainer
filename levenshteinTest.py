import tkinter as tk
import Levenshtein
import difflib

def compare_texts(original_text, user_transcription):
    # Calculate Levenshtein distance and similarity ratio
    distance = Levenshtein.distance(original_text, user_transcription)
    similarity = Levenshtein.ratio(original_text, user_transcription)

    # Generate differences using difflib
    diff = list(difflib.ndiff(original_text.split(), user_transcription.split()))

    return diff, distance, similarity

def display_text_with_errors(original_text, user_transcription):
    # Create a tkinter window
    root = tk.Tk()
    root.title("Speech Trainer")

    # Create a Text widget for displaying the text
    text_widget = tk.Text(root, wrap=tk.WORD, width=60, height=15, font=("Arial", 12))
    text_widget.pack(padx=10, pady=10)

    # Calculate the differences
    diff, distance, similarity = compare_texts(original_text, user_transcription)

    # Display results above the text
    result_label = tk.Label(root, text=f"Levenshtein Distance: {distance} | Similarity Ratio: {similarity:.2f}", font=("Arial", 10))
    result_label.pack(pady=5)

    # Insert the original text
    text_widget.insert(tk.END, "Original Text: \n")
    text_widget.insert(tk.END, original_text + "\n\n")

    text_widget.insert(tk.END, "User's Transcription: \n")

    # Highlight errors using difflib differences
    index = 0  # Start position for applying tags
    for word in diff:
        if word.startswith('-'):  # Deletion from user input (error)
            text_widget.insert(tk.END, word[2:] + " ", "error")  # Highlight the deleted word in red
        elif word.startswith('+'):  # Addition in user input (extra word)
            text_widget.insert(tk.END, word[2:] + " ", "addition")  # Highlight the added word in blue
        elif word.startswith(' '):  # Correct word
            text_widget.insert(tk.END, word[2:] + " ", "correct")  # Highlight the correct word in green

    # Tag configuration for highlighting errors and correct words
    text_widget.tag_config("error", foreground="red", font=("Arial", 12, "bold"))
    text_widget.tag_config("addition", foreground="blue", font=("Arial", 12, "italic"))
    text_widget.tag_config("correct", foreground="green", font=("Arial", 12))

    # Make the text widget non-editable
    text_widget.config(state=tk.DISABLED)

    # Run the Tkinter event loop
    root.mainloop()

original_text = "This is the correct text yes."
user_transcription = "This is te correct text tree holz yes."

display_text_with_errors(original_text, user_transcription)
