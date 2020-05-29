#!/usr/bin/python
from csv import reader
import csv
import numpy as np
import matplotlib.pyplot as plot

from peaks import calculate_peak

with open('ml/car.csv', 'r') as file:

    csv_reader = reader(file)
    lineNumber = 0
    plotNumber = 0
    plotstr = 'Plot: '
    linestr = 'Line: '

    for row in csv_reader:

        lineNumber = lineNumber + 1
        plotNumber = plotNumber + 1

        if not row:
            continue

        buff = list(map(float, row))

        plot.plot(buff)
        plot.ylabel('Voltage  ' + str(lineNumber))
        plot.show()

        print(linestr + str(lineNumber))
        print(plotstr + str(plotNumber))

        if(lineNumber > 20):
            break
        
    print("complated!")
