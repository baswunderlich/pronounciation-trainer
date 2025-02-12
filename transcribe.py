import whisper
import string

def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)

def transcribe_audio(audio_file):
    """
    Loads the small Whisper model, transcribes the given audio file,
    removes punctuation and converts the result to lowercase.
    
    Returns the cleaned transcription.
    """
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)
    transcription = result["text"]
    # Remove punctuation and convert to lowercase
    transcription_clean = remove_punctuation(transcription).lower()
    return transcription_clean

def calculate_score(transcription, reference_text):
    """
    Compares the transcription to the reference text.
    Both texts are cleaned (punctuation removed and converted to lowercase)
    and then split into words. The function returns the number of correct words,
    the total number of reference words, and the accuracy percentage.
    """
    # Clean the reference text
    reference_clean = remove_punctuation(reference_text).lower()
    
    # Split texts into words
    transcription_words = transcription.split()
    reference_words = reference_clean.split()
    
    # Compare word-by-word using zip (stops at the shortest list)
    correct_count = 0
    for ref_word, trans_word in zip(reference_words, transcription_words):
        if ref_word == trans_word:
            correct_count += 1
    
    total_reference_words = len(reference_words)
    score_percentage = (correct_count / total_reference_words) * 100 if total_reference_words > 0 else 0
    
    return correct_count, total_reference_words, score_percentage

if __name__ == "__main__":
    # Specify the audio file and reference text
    audio_file = "reference_test_withError.wav"
    reference_text = (
        "This is the reference text that should match what is spoken in the audio file. "
    )
    
    # Transcribe the audio file
    transcription = transcribe_audio(audio_file)
    print("Transcription (cleaned):")
    print(transcription)
    
    # Print the cleaned reference text
    reference_clean = remove_punctuation(reference_text).lower()
    print("\nReference text (cleaned):")
    print(reference_clean)
    
    # Calculate and print the score
    correct_count, total_reference_words, score_percentage = calculate_score(transcription, reference_text)
    print(f"\nScore: {correct_count} out of {total_reference_words} words correct.")
    print(f"Accuracy: {score_percentage:.2f}%")
