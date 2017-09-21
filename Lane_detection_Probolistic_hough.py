"""
Spyder Editor

Tanay - 7 April 2017.
"""
import math
import cv2
import numpy as np



"-----------------------------------------------------------------------------"
"-------------------- Automatic Threshold Detector for Canny------------------"
"-----------------------------------------------------------------------------"

# Automatic Image thresholds for the Canny Edge detector
def autocanny(image, sigma=0.33):
    
    #Computing the median of the image
    #v = np.median(image)
    v = 0.9*np.amax(image)
    
    # Selection of the lower and Upper thresholds
    lower = int(max(0, (1.0 - sigma)*v)) + 0
    upper = int(min(255, (1.0 +sigma)*v)) + 0
    edged = cv2.Canny(image, lower, upper)
    
    # Return the Edge Image
    return edged

"-----------------------------------------------------------------------------"
"------------------------- Color Selection -----------------------------------"
"-----------------------------------------------------------------------------"

def color_selection(image):
    # Input is the image from camera
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
      
    # The calibration values
    H_low = 0 
    S_low = 0
    V_low = 0
    H_high = 255
    S_high = 25
    V_high = 81
    
    # Create a boundry for the color selection
    lower = np.array([H_low,S_low,V_low])
    upper = np.array([H_high,S_high,V_high])

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)

    # Return HSV filtered image
    return output

"-----------------------------------------------------------------------------"
"-------------------------- Hough Transform - Simple -------------------------"
"-----------------------------------------------------------------------------"

def houghtransform_simple(edge, image, threshold, minLineLength, maxLineGap):
    # Hough Lines
    lines = cv2.HoughLinesP(edge,1,np.pi/180,threshold,minLineLength,maxLineGap)
        
    # Copy of the original Image
    image_cp = image.copy()
    
    if lines is not None:   
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(image_cp,(x1,y1),(x2,y2),(0,255,0),2)
        return(image_cp, 0)

    else:
         print("No Lines")
         return (image_cp, None)

"-----------------------------------------------------------------------------"
"-------------------- The start of the program -------------------------------"
"-----------------------------------------------------------------------------"

# Read the image
def lane_detection(image):        
    if image is None: raise ValueError("no image given to mark_lanes")
        
    "------------------------- Color Selection --------------------------------"    
    selection_image = color_selection(image)
    
    "------------------------- Smoothning of the image ------------------------" 
    # Gaussian smoothing
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(selection_image,(kernel_size, kernel_size), 0)


    "------------------------- Gradient Image ------------------------"
    laplacianx64f = cv2.Laplacian(blur_gray,cv2.CV_64F)
    abs_laplacianx64f = np.absolute(laplacianx64f)
    laplacian_8u = np.uint8(abs_laplacianx64f)
        
    "------------------------- Canny Edge Detection ---------------------------"     
    # Define our parameters for Canny and apply
    edges_img = autocanny(np.uint8(laplacian_8u))
    
    
    "------------------------- Smoothning of the image ------------------------" 
    # Gaussian smoothing
    kernel_size = 5
    edges_img = cv2.GaussianBlur(edges_img,(kernel_size, kernel_size), 0)
    
   
    "------------------------- Hough Transform ------------------------------------"
    threshold = 30
    minLineLength = 5
    maxLineGap = 5
    (line_image, steering) = houghtransform_simple(edges_img, image, threshold, minLineLength, maxLineGap)
  
    # Return the value of steering
    return (line_image, steering)
    
        
        
        
