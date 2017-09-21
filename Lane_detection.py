"""
Spyder Editor

Tanay - 7 April 2017.
"""
import math
import cv2
import numpy as np

"-----------------------------------------------------------------------------"
"-------------------- Region of Interest for the image to work-----------------"
def region_of_interest(img, vertices):
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

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
    S_low = 68
    V_low = 3
    H_high = 115
    S_high = 255
    V_high = 89
    
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

def houghtransform_simple(edge, image, threshold):
    # Hough Lines
    lines = cv2.HoughLines(edge, 1, np.pi/180, threshold)
        
    # Copy of the original Image
    image_cp = image.copy()
    
    # Parameters to calculate the average line    
    itr = 0
    x1_itr = 0
    x2_itr = 0
    y1_itr = 0
    y2_itr = 0
    
    if lines is not None:
        for line_params in lines[0]:
            # Clear the image and plot lines to the original image
            # image_cp = image.copy()
            #print("Lines", len(lines[0]))
            rho = line_params[0]
            theta = line_params[1]
            #print("Theta", math.degrees(theta))
            if(math.degrees(theta) < 60  or math.degrees(theta) > 120):
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
            
                # Print line for the Rho and Theta Values
                cv2.line(image_cp, (x1,y1), (x2,y2), (255,0,0), 2)
                 
                # Average of the lines
                itr = itr + 1
                x1_itr = x1_itr + x1
                x2_itr = x2_itr + x2
                y1_itr = y1_itr + y1
                y2_itr = y2_itr + y2
                #print("Rho", rho, "Theta", math.degrees(theta))
                
                if(itr > 6):
                    break
            
            # Average Line in Green Color        
            try:
                x1_itr = x1_itr / itr 
                x2_itr = x2_itr / itr 
                y1_itr = y1_itr / itr 
                y2_itr = y2_itr / itr 
                slope = math.atan2(y2_itr - y1_itr, x2_itr - x1_itr)
                slope = 90 - math.degrees(slope)
                cv2.line(image_cp, (x1_itr,y1_itr), (x2_itr,y2_itr), (0,255,0), 2)
            except:
                slope = 0                    
            
            return(image_cp, slope)
            
    else:
         print("No Lines")
         return (image_cp, None)

"-----------------------------------------------------------------------------"
"-------------------- The start of the program -------------------------------"
"-----------------------------------------------------------------------------"

# Read the image
def lane_detection(image):        
    if image is None: raise ValueError("no image given to mark_lanes")
    
    image = image[10:150, 40:280]    
    
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
    cv2.imshow('Edge Image',edges_img)
    
   
    "------------------------- Hough Transform ------------------------------------"
    threshold = 20
    (line_image, steering) = houghtransform_simple(edges_img, image, threshold)
  
    # Return the value of steering
    return (line_image, steering)
    
        
        
        
