import csv
import numpy as np
import time
import cv2
from time import strftime
import requests


import adafruit_dht
from board import *
# GPIO17 DHT22
SENSOR_PIN = D17

#relay
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)

dht22 = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)
temperature = dht22.temperature
humidity = dht22.humidity

cap = cv2.VideoCapture(0)
count = 0
while (True):
    
    ret , frame = cap.read()
    
    key = cv2.waitKey(100)

    
    timefile = strftime("%d_%m_%Y_%H-%M-%S")
    timedate = strftime("%d/%m/%Y")
    timehours = strftime("%H:%M:%S")
    targetlist = [timedate, timehours, temperature, humidity] 

    GPIO.output(4, True)

    if count == 30:
        GPIO.output(4, True)
        with open ('/home/pi/project/dist/datalog.csv', 'a') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(targetlist)
        cv2.imwrite( '/home/pi/project/dist/'+timefile + '.jpg', frame)

        #Http requests 
        objData = {'tem':temperature, 'hum':humidity ,'date':timedate, 'time':timehours}
        url = 'http://192.168.1.60:5000/'
        my_img = {'files[]': open('/home/pi/project/dist/'+timefile + '.jpg', 'rb')},{'json':objData}
        img = requests.post(url+'upload', files = my_img)
        # tem_hum = requests.post(url+'tem_hum', json = objData)
        

        break
    count+=1

GPIO.output(4, False)
cv2.waitKey(1000)
GPIO.output(4, False)
cap.release()