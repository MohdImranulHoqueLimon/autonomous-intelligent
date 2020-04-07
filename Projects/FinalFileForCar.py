#!/usr/bin/python

import threading
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import csv
import numpy as np
#from scipy.fftpack import fft
from numpy.fft import fft
import xlrd
from scipy.signal import find_peaks

#rp_s = scpi.scpi('192.168.128.1')

loc = ("files/Car_Data.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

writer = csv.writer(open("files/carpeak.csv", 'a'))

def getData():
   #94
   for i in range(100):
    print(i)
    #print(sheet.row_values(i))
    #buff_string=sheet.row_values(i)
    buff_string = sheet.col_values(i)
    print(buff_string)
    #buff_string = buff_string.split(',')
    buff = list(map(float, buff_string))
    filteredList = []
    for idx, x in enumerate(buff):
        if idx > 5000:
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

    test = ["car"]

    #writer.writerow(np.append(peaks, test))

    #print(peaks)
    plot.plot(fft_ps)
    plot.plot(np.zeros_like(fft_ps), "--", color="gray")
    plot.show()


#print(a_string)
    #dd=np.fft.fft(a_string)
    #print(dd)


getData()