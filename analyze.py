import wave
import numpy as np
import matplotlib.pyplot as plt
import sys

# Open WAV file
wav_obj = wave.open(sys.argv[1], 'rb')

# Get basic properties
sample_freq = wav_obj.getframerate()  # Sample rate
n_samples = wav_obj.getnframes()  # Total number of frames
t_audio = n_samples / sample_freq  # Duration in seconds
n_channels = wav_obj.getnchannels()  # Mono (1) or Stereo (2)

print(f"Sample Rate: {sample_freq} Hz")
print(f"Number of Samples: {n_samples}")
print(f"Duration: {t_audio:.2f} seconds")
print(f"Channels: {n_channels}")

# Read audio data
signal_wave = wav_obj.readframes(n_samples)
signal_array = np.frombuffer(signal_wave, dtype=np.int16)

# Stereo handling: separate left & right channels
if n_channels == 2:
    l_channel = signal_array[0::2]
    r_channel = signal_array[1::2]
    signal_array = l_channel  # Default to left channel for visualization
else:
    l_channel = signal_array
    r_channel = None  # No right channel in mono

# Time axis correction
times = np.linspace(0, t_audio, num=len(l_channel))

# --- Create a single figure with 2 subplots (2 rows, 1 column) ---
fig, axes = plt.subplots(2, 1, figsize=(9, 6))  # 2 rows, 1 column

# --- Plot Waveform in First Subplot ---
axes[0].plot(times, l_channel, label="Left Channel", color="blue")
if r_channel is not None:
    axes[0].plot(times, r_channel, label="Right Channel", color="red", alpha=0.7)
axes[0].set_title('Waveform')
axes[0].set_ylabel('Signal Value')
axes[0].set_xlabel('Time (s)')
axes[0].set_xlim(0, t_audio)
axes[0].legend()

# --- Plot Spectrogram in Second Subplot ---
axes[1].specgram(l_channel, Fs=sample_freq, vmin=-20, vmax=50)
axes[1].set_title('Spectrogram (Left Channel)')
axes[1].set_ylabel('Frequency (Hz)')
axes[1].set_xlabel('Time (s)')
axes[1].set_xlim(0, t_audio)
fig.colorbar(plt.cm.ScalarMappable(), ax=axes[1], label="Intensity (dB)")  # Colorbar for spectrogram

# --- Adjust layout and show figure ---
plt.tight_layout()
plt.show()
