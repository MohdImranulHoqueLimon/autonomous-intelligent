#!/usr/bin/python
from csv import reader
import csv
import numpy as np
import matplotlib.pyplot as plot

from peaks import calculate_peak

with open('ml/human.csv', 'r') as file:
    csv_reader = reader(file)
    for row in csv_reader:
        if not row:
            continue
        buff = list(map(float, row))

        mean = np.mean(buff)
        variance = np.var(buff)

        #m = sum(buff) / len(buff)
        #v = sum((xi - m) ** 2 for xi in buff) / len(buff)

        plot.plot(buff)
        plot.ylabel('Voltage')
        plot.show()

        peaks = calculate_peak(buff)
        test = peaks.get('peak_heights')
        min=test.min()
        rowtest = [test.min(), test.max(),test.shape[0], mean, variance]
        #1 for wall
        test = [2]
        writer = csv.writer(open("ml/features.csv", 'a'))
        writer.writerow(np.append(rowtest, test))
