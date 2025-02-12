import whisper
import string
import numpy as np
import librosa
import soundfile as sf

def remove_punctuation(text):
    """
    Remove punctuation from text.
    """
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)

def add_noise_to_audio(audio_file, noise_level=0.05):
    """
    Loads an audio file, adds white noise to it, and saves the noisy audio.
    
    Parameters:
        audio_file (str): Path to the original audio file.
        noise_level (float): Scaling factor for the noise amplitude.
        
    Returns:
        str: Path to the noisy audio file.
    """
    # Load the original audio file (preserving its original sampling rate)
    audio, sr = librosa.load(audio_file, sr=None)
    
    # Generate white noise (same length as the audio)
    noise = np.random.randn(len(audio))
    
    # Add noise to the audio signal
    noisy_audio = audio + noise_level * noise
    
    # Ensure the signal remains in the valid range [-1, 1]
    noisy_audio = np.clip(noisy_audio, -1.0, 1.0)
    
    # Save the noisy audio to a new file
    noisy_file = "noisy_" + audio_file
    sf.write(noisy_file, noisy_audio, sr)
    return noisy_file

def transcribe_audio(audio_file):
    """
    Loads the small Whisper model, transcribes the given audio file,
    removes punctuation, and converts the result to lowercase.
    
    Returns:
        str: The cleaned transcription.
    """
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)
    transcription = result["text"]
    transcription_clean = remove_punctuation(transcription).lower()
    return transcription_clean

def getTranscript():
    original_audio_file = "output.wav"
    
    noisy_audio_file = add_noise_to_audio(original_audio_file, noise_level=0.005)
    print(f"Added noise to the audio file, saved as: {noisy_audio_file}")
    
    transcription = transcribe_audio(noisy_audio_file)
    return transcription