import numpy as np
import xlrd
import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks

def fft_transform ():
    loc = ("humanRead.xls")

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    sheet.cell_value(0, 0)
    window =sheet.row_values(0)
    #reading first row in excel file of wall data
    print(window)
    #window_data
    fft_data = []
    fft_freq = []
    power_spec = []

    #for window in window_data:

    fftd_window = np.fft.fft(window)
    fft_data.append(fftd_window)

    freq  = np.fft.fftfreq(np.array(window).shape[-1], d=0.01)
    fft_freq.append(freq )

    fft_ps = np.abs(fftd_window)**2
    power_spec.append(fft_ps)

    print(fftd_window)
    print(fft_data)
    print(fft_freq)
    print(power_spec)

    peaks, _ = find_peaks(fft_ps, height=0)
    plt.plot(fft_ps)
    plt.plot(np.zeros_like(fft_ps), "--", color="gray")
    plt.show()
    #return fft_data, fft_freq, power_spec

fft_transform()