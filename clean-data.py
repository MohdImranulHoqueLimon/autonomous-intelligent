#!/usr/bin/python
from csv import reader
import csv
import numpy as np
import matplotlib.pyplot as plot

from peaks import calculate_peak

with open('ml/human.csv', 'r') as file:

    csv_reader = reader(file)
    lineNumber = 0
    plotNumber = 0
    plotstr = 'Plot: '
    linestr = 'Line: '

    for row in csv_reader:

        lineNumber = lineNumber + 1
        count = 0

        if(lineNumber > 80):
            if not row:
                continue

            count = count + 1
            plotNumber = plotNumber + 1
            buff = list(map(float, row))

            plot.plot(buff)
            plot.ylabel('Voltage  Line: ' + str(lineNumber) + '  Plot: ' + str(plotNumber))
            plot.show()

            print(linestr + str(lineNumber))
            print(plotstr + str(plotNumber))
        
    print("complated!")
