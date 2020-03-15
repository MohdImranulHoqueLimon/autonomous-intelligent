import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import threading
import csv
import collections

rp_s = scpi.scpi('192.168.128.1')

def getData():
    threading.Timer(3, getData).start()

    rp_s.tx_txt('ACQ:START')
    #rp_s.tx_txt('ACQ:TRIG NOW')
    rp_s.tx_txt('SOUR1:TRIG:SOUR DIO0_P')
    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break

    rp_s.tx_txt('ACQ:SOUR1:DATA?')
    buff_string = rp_s.rx_txt()
    print(buff_string)
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = list(map(float, buff_string))
    plot.plot(buff)
    plot.ylabel('Voltage')
    plot.show()

    writer = csv.writer(open("human.csv", 'a'))
    writer.writerow(buff_string)

getData()
