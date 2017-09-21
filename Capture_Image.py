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

#import Lane_detection_Probolistic_hough as ld
import Lane_detection as ld
import arduinoCom

class KalmanFilter:
    def __init__(self, miu_0, sigma_0, Q, R):
        self.miu = miu_0
        self.sigma = sigma_0
        self.Q = Q
        self.R = R
                
    def predict(self, miu):
        self.miu_hat = self.miu
        self.sigma_hat = self.sigma + self.Q
        
        return self.miu_hat
        
        
    def update(self, measure):
        # Kalman Gain
        self.K = self.sigma_hat / (self.sigma_hat + self.R)
        # Prediction error
        self.sigma = (1 - self.K)*self.sigma_hat
        # New Values
        self.miu = self.miu_hat + self.K * (measure - self.miu_hat)
        
        return self.miu
    
# Kalman Filter for the steering
kf = KalmanFilter(0, 10, 0.1, 10)
steering = 0

"-----------------------------------------------------------------------------"
"-------------------- The start of the program -------------------------------"
"-----------------------------------------------------------------------------"
# Parameters
resolution = (320, 240)
a1 = -0.3
a2 = -0.45
a3 = -0.55

#Camera Initialization
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = resolution)

#Arduino Initialization
#Pin configuration type BCM
GPIO.setmode(GPIO.BCM)
#Create an Arduino Object which has base code for communication between Pi and Arduino
arduino = arduinoCom.Arduino()

# Allow Camera and Arduino to warmup
time.sleep(2)

"------------------------- Connection To Arduino -----------------------------"
#Try connecting to Ardunio from any of the USB ports
for i in range (10):
    if arduino.connect() == 1:
        print 'connection established'
        break
    else:
        print 'Connection failed'

time.sleep(1)

arduino.set_value(0, 0)
time.sleep(1)

"------------------------- Image Caputre -------------------------------------"
# Capture Frames from Camera
for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
    # grab the raw Numpy array representing the image, then initialize the timestamp and occupy image
    image = frame.array
    image_cp = image
    
   
    # Line detection
    (output , angle)= ld.lane_detection(image_cp)
    cv2.imshow('Output Image',output)  

        
    # Command to the arduino for steering
    cmd_time = time.time()
    while (time.time() - cmd_time) < 0.25:
        if angle is not None:
            if (angle > 90):
                angle = angle - 180
                
            "------------------ Kalman Filter for the steering angle ----------------------"
            if(angle is None):
                steering = kf.predict(steering)
            else:
                kf.predict(steering)
                steering = kf.update(angle)
                steering = round(steering, 2)

            
            # Angular Velocity
            if(math.fabs(steering) < 10):
                angular_vel = a1*math.sin(math.radians(steering))
                linear_vel = 0.06
		case = 1
            elif (math.fabs(steering) < 20):
                angular_vel = a2*math.sin(math.radians(steering))
                linear_vel = 0.075
		case = 2	
            else:
                angular_vel = a3*math.sin(math.radians(steering))
		linear_vel = 0.06
		case = 3
            print("Vel : ", linear_vel, "Case : ", case, "Steering :",steering)
            arduino.set_value(linear_vel, angular_vel)
        else:
            break
        
        
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


