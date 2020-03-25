#!/usr/bin/python

import threading
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import numpy as np
import csv
from scipy.signal import find_peaks
from MergingAllDataSehrish import run_ml_with_live_data,train_system

rp_s = scpi.scpi('192.168.128.1')

def getData():
    threading.Timer(3, getData).start()
    wave_form = 'sine'
    freq = 10000
    ampl = 2

    rp_s.tx_txt('GEN:RST')
    rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))
    rp_s.tx_txt('SOUR1:BURS:NCYC 2')
    rp_s.tx_txt('OUTPUT1:STATE ON')
    rp_s.tx_txt('SOUR1:BURS:STAT ON')
    rp_s.tx_txt('SOUR1:TRIG:SOUR EXT_PE')

    rp_s.tx_txt('ACQ:DEC 64')
    rp_s.tx_txt('ACQ:TRIG:LEVEL 100')
    rp_s.tx_txt('ACQ:START')
    rp_s.tx_txt('ACQ:TRIG EXT_PE')
    rp_s.tx_txt('ACQ:TRIG:DLY 9000')

    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break

    rp_s.tx_txt('ACQ:SOUR1:DATA?')
    buff_string = rp_s.rx_txt()
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = list(map(float, buff_string))

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

    plot.plot(buff)
    plot.ylabel('Voltage')
    plot.show()
    peakList = list()
    peakList=peaks.tolist()
    peakList.sort(reverse=True)
    slice = peakList[:100]
    run_ml_with_live_data(trainModel,slice)

trainModel=train_system()
getData()
