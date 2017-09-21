# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 17:08:49 2017

@author: pi
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

"-----------------------------------------------------------------------------"
"-------------------- Automatic Threshold Detector for Canny------------------"
"-----------------------------------------------------------------------------"

# Automatic Image thresholds for the Canny Edge detector
def autocanny(image, sigma=0.33):

    #print("Image_Min:", np.amin(image))
    #print("Image_Max:", np.amax(image))    
    #Computing the median of the image
    #v = np.median(image)
    v = 0.9*np.amax(image)
        
    # Selection of the lower and Upper thresholds
    lower = int(max(0, (1.0 - sigma)*v)) + 0
    upper = int(min(255, (1.0 +sigma)*v)) + 0
    edged = cv2.Canny(image, lower, upper)
    # print("Lowe:", lower, "Upper:", upper)
    
    # Return the Edge Image
    return edged


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



# Allow Camera to warmup
time.sleep(0.1)
#cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)

"------------------------- Trackbar definition --------------------------------"
def nothing(x):
    pass

cv2.namedWindow('Trackbar')
# Create trackbar for selection of the boundry
cv2.createTrackbar('H_low','Trackbar',0,360,nothing)
cv2.createTrackbar('S_low','Trackbar',0,255,nothing)
cv2.createTrackbar('V_low','Trackbar',0,255,nothing)
cv2.createTrackbar('H_high','Trackbar',0,255,nothing)
cv2.createTrackbar('S_high','Trackbar',0,255,nothing)
cv2.createTrackbar('V_high','Trackbar',0,255,nothing)


"------------------------- Color Selection ------------------------------------"

    
# Capture Frames from Camera
for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
    # grab the raw Numpy array representing the image, then initialize the timestamp and occupy image
    image = frame.array
    image = image[10:150, 40:280] 
    
    # Show the image
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # get current positions of four trackbars
    H_low = cv2.getTrackbarPos('H_low','Trackbar')
    S_low = cv2.getTrackbarPos('S_low','Trackbar')
    V_low = cv2.getTrackbarPos('V_low','Trackbar')
    H_high = cv2.getTrackbarPos('H_high','Trackbar')
    S_high = cv2.getTrackbarPos('S_high','Trackbar')
    V_high = cv2.getTrackbarPos('V_high','Trackbar')
    
    # The calibration values
    #H_low = 8 
    #S_low = 82
    #V_low = 6
    #H_high = 37
    #S_high = 255
    #V_high = 51
    
    # Create a boundry for the color selection
    lower = np.array([H_low,S_low,V_low])
    upper = np.array([H_high,S_high,V_high])    
    
    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image_hsv, lower, upper)
    output = cv2.bitwise_and(image_hsv, image_hsv, mask=mask)

    "------------------------- Gradient Image ------------------------"
    laplacianx64f = cv2.Laplacian(output,cv2.CV_64F)
    abs_laplacianx64f = np.absolute(laplacianx64f)
    laplacian_8u = np.uint8(abs_laplacianx64f)

    "------------------------- Smoothning of the image ------------------------" 
    # Gaussian smoothing
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(laplacian_8u,(kernel_size, kernel_size), 0)

    "------------------------- Canny Edge Detection ---------------------------"     
    # Define our parameters for Canny and apply
    edges_img = autocanny(np.uint8(blur_gray))
    
    # show images
    #cv2.namedWindow('Output')
    #cv2.imshow('Output',output)
    #cv2.namedWindow('Original Image')
    #cv2.imshow('Original Image',image)
    #cv2.namedWindow('Laplacian Image')
    #cv2.imshow('Laplacian Image', blur_gray)
    cv2.namedWindow('Edge Image')
    cv2.imshow('Edge Image', output)   
    # If Enter is pressed, then break from loop
    key = cv2.waitKey(1) & 0xFF
    if key == 10:
        print("Exit")
        break
    
    # Clear the stream for the next frame
    rawCapture.truncate(0)
    

#rawCapture.truncate(0)
# Close all the windows and release resources for camera
cv2.destroyWindow("Original Image")
cv2.destroyAllWindows()
camera.close()
print("Bye Tanay")

