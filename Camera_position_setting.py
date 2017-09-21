# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:39:54 2017

@author: pi
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 17:08:49 2017

@author: pi
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as GPIO
import math

"-----------------------------------------------------------------------------"
"-------------------- The start of the program -------------------------------"
"-----------------------------------------------------------------------------"
# Parameters
resolution = (320, 240)

#Camera Initialization
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = resolution)

#Arduino Initialization
#Pin configuration type BCM
GPIO.setmode(GPIO.BCM)

# Allow Camera and Arduino to warmup
time.sleep(2)

"------------------------- Image Caputre -------------------------------------"
# Capture Frames from Camera
for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
    # grab the raw Numpy array representing the image, then initialize the timestamp and occupy image
    image = frame.array
    image_cp = image
    image_cp = image_cp[10:150, 40:280]
    cv2.imshow('Output Image',image_cp)  
         
        
    # If Enter is pressed, then break from loop
    key = cv2.waitKey(1) & 0xFF
    if key == 10:
        print("Exiting!!")
        break
    
    # Clear the stream for the next frame
    rawCapture.truncate(0)
    

# Close all the windows and release resources for camera
cv2.destroyAllWindows()
camera.close()
print("Bye Tanay")


