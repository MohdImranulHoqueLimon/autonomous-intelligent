import numpy as np
import xlrd
import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
from peaks import calculate_peak
import csv

loc = ("files/Car_Data.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
sheet = wb.sheet_by_index(0)

def fft_transform ():
    for col in range(sheet.ncols):
         window =sheet.col_values(col)
         #reading first row in excel file of wall data
         #print(window)
         #plt.plot(window)
         #plt.ylabel('Voltage')
         #plt.show()
         buff = list(map(float, window))
         mean = np.mean(buff)
         variance = np.var(buff)
         peaks = calculate_peak(buff)
         test = peaks.get('peak_heights')
         min = test.min()
         rowtest = [test.min(), test.max(), test.shape[0]]
         # 3 for car
         test = [3]
         writer = csv.writer(open("ml/features.csv", 'a'))
         writer.writerow(np.append(rowtest, test))


fft_transform()