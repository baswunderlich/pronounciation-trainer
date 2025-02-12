import pyaudio
import wave
import threading
import textgenerator
import transcribe

# Global variables
p = pyaudio.PyAudio()  # Initialize PyAudio once
stream = None
stop = False
t1 = None

def start_recording():
    global t1
    t1 = threading.Thread(target=record)
    t1.start()

def record():
    global stop, stream
    stop = False
    chunk = 1024  # Buffer size
    sample_format = pyaudio.paInt16  # 16-bit audio
    channels = 1
    fs = 44100  # Sample rate
    filename = "output.wav"

    print("Recording...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    while not stop:
        try:
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print("Stream error:", e)
            break

    # Close stream
    if stream is not None:
        stream.stop_stream()
        stream.close()
        stream = None  # Reset stream

    print("Finished recording")

    # Save as WAV file
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b"".join(frames))
    wf.close()

def stop_recording():
    global stop
    stop = True
    
    text_original = textgenerator.current_text
    transcript = transcribe.getTranscript()
    print(f"transcript: {transcript}")
    print(levenshtein("The tree is red", "the tree is red"))
    
    result = levenshtein(text_original, transcript)
    print(result)
    print(len(text_original.split(" ")))
    print("Score:", calc_score(text_original, transcript))
    

def calc_score(text_original, text_recorded) -> float:
    score = (len(text_original.split(" "))-result)/len(text_original.split(" "))
    print("Score:", score)
    return score


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2.split(" ")) + 1)
    for i, c1 in enumerate(s1.split(" ")):
        current_row = [i + 1]
        for j, c2 in enumerate(s2.split(" ")):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    print("Stopping recording...")
    return previous_row[-1]
