#!/usr/bin/python

import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import csv
import collections

rp_s = scpi.scpi('192.168.128.1')

rp_s.tx_txt('ACQ:START')
rp_s.tx_txt('ACQ:TRIG NOW')

while 1:
    rp_s.tx_txt('ACQ:TRIG:STAT?')
    if rp_s.rx_txt() == 'TD':
        break

rp_s.tx_txt('ACQ:SOUR1:DATA?')
buff_string = rp_s.rx_txt()
buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
buff = list(map(float, buff_string))

writer = csv.writer(open("wall.csv", 'a'))
writer.writerow(buff_string)