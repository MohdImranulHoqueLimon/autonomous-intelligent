#!/usr/bin/python

import threading
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot
import csv
import numpy as np
from scipy import pi
from scipy.fftpack import fft
import xlrd

#rp_s = scpi.scpi('192.168.128.1')

def getData():
    loc = ("wallRead.xls")

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    sheet.cell_value(0, 0)

    print(sheet.row_values(2))
    a_string=sheet.row_values(2)
    print(a_string)
    dd=np.fft.fft(a_string)
    print(dd)


getData()