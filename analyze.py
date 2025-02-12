import wave
import numpy as np
import matplotlib.pyplot as plt
import sys

wav_obj = wave.open(sys.argv[1], 'rb')

sample_freq = wav_obj.getframerate()
print(str(sample_freq))

n_samples = wav_obj.getnframes()
print(str(n_samples))

t_audio = n_samples/sample_freq
print(str(t_audio))

n_channels = wav_obj.getnchannels()
print(str(n_channels))

signal_wave = wav_obj.readframes(n_samples)
signal_array = np.frombuffer(signal_wave, dtype=np.int16)

l_channel = signal_array[0::2]
r_channel = signal_array[1::2]

times = np.linspace(0, n_samples/sample_freq, num=n_samples)
print("times", str(len(times)))
print("len(l_channel)", str(len(l_channel)))

plt.figure(figsize=(15, 5))
plt.plot(times, signal_array)
plt.title('Left Channel')
plt.ylabel('Signal Value')
plt.xlabel('Time (s)')
plt.xlim(0, t_audio)
plt.show()

plt.figure(figsize=(15, 5))
plt.specgram(signal_array, Fs=sample_freq, vmin=-20, vmax=50)
plt.title('Left Channel')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.xlim(0, t_audio)
plt.colorbar()
plt.show()