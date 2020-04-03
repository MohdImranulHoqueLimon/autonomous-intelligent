#!/usr/bin/python
import sys
import threading
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import random
from csv import reader
import csv
import numpy as np
from peaks import calculate_peak


with open('ml/human.csv', 'r') as file:
    csv_reader = reader(file)
    for row in csv_reader:
        if not row:
            continue
        buff = list(map(float, row))
        peaks = calculate_peak(buff)
        test = peaks.get('peak_heights')
        min=test.min()
        rowtest = [test.min(), test.max(),test.shape[0]]
        #1 for wall
        test = [2]
        writer = csv.writer(open("ml/features.csv", 'a'))
        writer.writerow(np.append(rowtest, test))


        #floatRow = list()
        #for cell in row:
            #if cell != '':
                #floatRow.append(float(cell))

        #peaks = calculate_peak(floatRow)


#buff_string = buff_string.replace(",", ".").split('	')



#buff = list(map(float, buff_string))

#plot.plot(buff)
#plot.ylabel('Voltage')
#plot.show()
