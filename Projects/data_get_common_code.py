#!/usr/bin/python

import threading
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import csv
from peaks import calculate_peak

rp_s = scpi.scpi('192.168.128.1')

def getData():
    try:
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
        peaks = calculate_peak(buff)
        writer = csv.writer(open("ml/human.csv", 'a'))
        writer.writerow(peaks)

        plot.plot(buff)
        plot.ylabel('Voltage')
        plot.show()
    except:
        print("An exception occurred")


getData()