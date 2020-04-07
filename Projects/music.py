import pygame
import threading
import datetime

def kuchtobolo():
    threading.Timer(5.0, kuchtobolo).start()
    try:
       f = open("guru99.txt","a+")
       dt = datetime.datetime.now()
       date_string = dt.strftime('%m/%d/%Y %h:%m:%s' + "\n")
       
       f.write(date_string)
    except:
        print("An exception occurred")

kuchtobolo()
