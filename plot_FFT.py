import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# insert the audio file (1 tick/hit)
audio_data, _ = sf.read("audio_file.wav")

# plot the audio signal (time)
plt.subplot(1, 2, 1)
plt.plot(audio_data)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Time Domain')

# perform Fast Fourier Transform (FFT)
fft_result = np.fft.fft(audio_data)

# absolute values of the result
fft_abs = np.abs(fft_result)

# plot the absolute values (frequency)
plt.subplot(1, 2, 2)
plt.plot(fft_abs)
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.title('Frequency Domain')

# layout and plot
plt.tight_layout()
plt.show()
