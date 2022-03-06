import numpy as np
import time
import cv2
from time import strftime
cap = cv2.VideoCapture(0)


#relay
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)

while (True):
    GPIO.output(4, True)
    ret , frame = cap.read()
    cv2.imshow("Output",frame)
    
    key = cv2.waitKey(1)
    if key == ord("c"):
        timefile = strftime("%d_%m_%Y_%H-%M-%S")
        cv2.imwrite( timefile + '.jpg', frame)
    if key & 0xFF == ord("e"):
        GPIO.output(4, False)
        break
    


cap.release()
cv2.destroyAllWindows

