import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def calculate_peak(buff):
    filteredList = []
    for idx, x in enumerate(buff):
        if idx > 2500:
            filteredList.append(x)

    fft_data = []
    fft_freq = []
    power_spec = []
    fftd_window = np.fft.fft(filteredList)
    fft_data.append(fftd_window)
    freq = np.fft.fftfreq(np.array(filteredList).shape[-1], d=0.01)
    fft_freq.append(freq)
    fft_ps = np.abs(fftd_window) ** 2
    power_spec.append(fft_ps)
    peaks, _ = find_peaks(fft_ps, height=0)

    plt.plot(fft_ps)
    plt.plot(np.zeros_like(fft_ps), "--", color="gray")
    plt.show()

    return peaks