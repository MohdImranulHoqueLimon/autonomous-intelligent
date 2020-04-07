from csv import reader
from math import sqrt
from math import exp
from math import pi
#import matplotlib.pyplot as plot
from peaks import calculate_peak
import sys
import threading
import redpitaya_scpi as scpi
import os
import pygame
import paramiko
#from pexpect import pxssh


ssh_connect = 0

def ssh_test():
    s = pxssh.pxssh()
    if not s.login ('192.168.128.1', 'root', 'root'):
        print ("SSH session failed on login.")
        #print str(s)
    else:
        print ("SSH session login successful")
        global ssh_connect
        ssh_connect = 1
        s.sendline ('ls -l')
        s.prompt()         # match the prompt
        #print s.before     # print everything before the prompt.
        s.logout()
    return s

totalTest = 50
def ssh_connection():
    try:
        REDPITAYA_HOST_IP = "192.168.128.1"
        userName = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        test = ssh.connect(REDPITAYA_HOST_IP, username=userName, password=password)
        stdin, stdout, stderr = ssh.exec_command("ls -a")
        global ssh_connect
        ssh_connect = 1
        #lines = stdout.readlines()
    except:
        print("An exception occurred")

def printLabel(label):
    if label == 1.0:
        print('Wall')
        playMusic("/home/pi/wall.mp3")
    if label == 2.0:
        print('Human')
        playMusic("/home/pi/human.mp3")
    if label == 3.0:
        print('car')
        playMusic("/home/pi/car.mp3")

def playMusic(path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    except:
        print("An exception occurred")

def load_csv(filename, allData):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            row = list(map(float, row))
            allData.append(row)
    return allData

# Convert string column to integer
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
        print('[%s] => %d' % (value, i))
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup

# Split dataset by class then calculate statistics for each row
def summarize_by_class(dataset):
    separated = separate_by_class(dataset)
    summaries = dict()
    for class_value, rows in separated.items():
        summaries[class_value] = summarize_dataset(rows)
    return summaries

# Calculate the mean, stdev and count for each column in a dataset
def summarize_dataset(dataset):
    summaries = [(mean(column), stdev(column), len(column)) for column in zip(*dataset)]
    del (summaries[-1])
    return summaries

# Calculate the mean of a list of numbers
def mean(numbers):
    return sum(numbers) / float(len(numbers))

# Calculate the standard deviation of a list of numbers
def stdev(numbers):
    avg = mean(numbers)
    variance = sum([(x - avg) ** 2 for x in numbers]) / float(len(numbers) - 1)
    return sqrt(variance)

# Split the dataset by class values, returns a dictionary
def separate_by_class(dataset):
    separated = dict()
    for i in range(len(dataset)):
        vector = dataset[i]
        class_value = vector[-1]
        if (class_value not in separated):
            separated[class_value] = list()
        separated[class_value].append(vector)
    return separated

# Calculate the probabilities of predicting each class for a given row
def calculate_class_probabilities(summaries, row):
    total_rows = sum([summaries[label][0][2] for label in summaries])
    probabilities = dict()
    for class_value, class_summaries in summaries.items():
        probabilities[class_value] = summaries[class_value][0][2] / float(total_rows)
        for i in range(len(class_summaries)):
            mean, stdev, _ = class_summaries[i]
            probabilities[class_value] *= calculate_probability(row[i], mean, stdev)
    return probabilities

# Calculate the Gaussian probability distribution function for x
def calculate_probability(x, mean, stdev):
    exponent = exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
    return (1 / (sqrt(2 * pi) * stdev)) * exponent


# Predict the class for a given row
def predict(summaries, row):
    probabilities = calculate_class_probabilities(summaries, row)
    best_label, best_prob = None, -1
    for class_value, probability in probabilities.items():
        if best_label is None or probability > best_prob:
            best_prob = probability
            best_label = class_value
    return best_label

# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

featuresData = 'ml/features.csv'
trainignData = list()
trainignData = load_csv(featuresData, trainignData)

# fit model
model = summarize_by_class(trainignData)



#ssh_test()
ssh_connection()

def getData():
    try:
        print(ssh_connect)
        if ssh_connect == 0:
            ssh_connection()
        else:
            rp_s = scpi.scpi('192.168.128.1')
            threading.Timer(6, getData).start()
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

            #plot.plot(buff)
            #plot.ylabel('Voltage')
            #plot.show()

            test = peaks.get('peak_heights')
            incomingData = [test.min(), test.max(),test.shape[0]]

            label = predict(model, incomingData)
            printLabel(label)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

getData()