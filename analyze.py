import wave
import numpy as np
import matplotlib.pyplot as plt

def generate_plot(wav_file):
    """
    Reads a WAV file and plots both its waveform (top) and spectrogram (bottom).
    Correctly links the colorbar to the spectrogram's intensity (dB) range.
    """
    # --- Open WAV file ---
    wav_obj = wave.open(wav_file, 'rb')

    # --- Basic properties ---
    sample_freq = wav_obj.getframerate()  # Sample rate in Hz
    n_samples   = wav_obj.getnframes()    # Total number of frames
    t_audio     = n_samples / sample_freq # Duration in seconds
    n_channels  = wav_obj.getnchannels()  # Mono (1) or Stereo (2)

    print(f"Sample Rate   : {sample_freq} Hz")
    print(f"Number of Samples: {n_samples}")
    print(f"Duration      : {t_audio:.2f} seconds")
    print(f"Channels      : {n_channels}")

    # --- Read audio data ---
    signal_wave = wav_obj.readframes(n_samples)
    signal_array = np.frombuffer(signal_wave, dtype=np.int16)

    # --- Stereo vs Mono Handling ---
    if n_channels == 2:
        # Separate left/right channels
        l_channel = signal_array[0::2]
        r_channel = signal_array[1::2]
        # Use left channel by default for plotting
        signal_array = l_channel
    else:
        l_channel = signal_array
        r_channel = None

    # --- Generate time axis ---
    times = np.linspace(0, t_audio, num=len(l_channel))

    # --- Create figure & axes ---
    fig, axes = plt.subplots(2, 1, figsize=(9, 6))  # 2 rows, 1 column

    # --- Plot waveform ---
    axes[0].plot(times, l_channel, label="Left Channel", color="blue")
    if r_channel is not None:
        axes[0].plot(times, r_channel, label="Right Channel", color="red", alpha=0.7)
    axes[0].set_title('Waveform')
    axes[0].set_ylabel('Signal Value')
    axes[0].set_xlabel('Time (s)')
    axes[0].set_xlim(0, t_audio)
    axes[0].legend()

    # --- Plot spectrogram ---
    # specgram() returns (Pxx, freqs, bins, im), so capture 'im' for colorbar
    Pxx, freqs, bins, im = axes[1].specgram(
        l_channel,
        Fs=sample_freq,
        vmin=-20,     # lower dB limit for color scale
        vmax=50       # upper dB limit for color scale
    )
    axes[1].set_title('Spectrogram (Left Channel)')
    axes[1].set_ylabel('Frequency (Hz)')
    axes[1].set_ylim(0, 12000)  # Force y-axis to show up to 12 kHz
    axes[1].set_xlabel('Time (s)')
    axes[1].set_xlim(0, t_audio)

    # --- Attach colorbar using the spectrogram image object ---
    fig.colorbar(im, ax=axes[1], label="Intensity (dB)")

    # --- Final layout tweaks ---
    plt.tight_layout()

    # Return the figure object (e.g., for saving or further manipulation)
    return fig

# Example usage:
if __name__ == "__main__":
    fig = generate_plot("example.wav")  # <-- Replace with your own .wav filename
    plt.show()  # Show the figure window
