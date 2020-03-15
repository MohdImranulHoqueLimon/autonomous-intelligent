#!/usr/bin/python

import threading
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import csv
import numpy as np
from scipy import pi
from scipy.fftpack import fft

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

    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break

    rp_s.tx_txt('ACQ:SOUR1:DATA?')
    buff_string = rp_s.rx_txt()
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = list(map(float, buff_string))

    with open('wall.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

    #test = np.fft(buff_string)
    #writer = csv.writer(open("human.csv", 'a'))
    #writer.writerow(buff_string)

    sample_rate = 16384
    N = (1 - 0) * sample_rate
    #it was 2 which is 2 second 512
    time = np.linspace(0, 2, N)
    frequency = np.linspace(0.0,8192 , int(N / 2))
    freq_data = fft(buff)
    y = 2 / N * np.abs(freq_data[0:np.int(N / 2)])

    plot.plot(frequency, y)
    plot.title('Frequency domain Signal')
    plot.xlabel('Frequency in Hz')
    plot.ylabel('Amplitude')
    plot.show()



   # plot.plot(buff)
    #plot.ylabel('Voltage')
    #plot.show()

getData()