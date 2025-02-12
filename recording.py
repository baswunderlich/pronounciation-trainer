import pyaudio
import wave
import threading

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
    print("Stopping recording...")
