# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

##print("HellO Anaconda")

import cv2
import time   ##give camera time before code executes
import numpy as np




cap=cv2.VideoCapture(0) ##for no. of camera
time.sleep(5)

background=0

for i in range(60):  ## 60 iteration so that it can capture the background slowly and clear
    ret,background=cap.read()     ####returns the image viz is captured and return value (true)


background=np.flip(background, axis=1)


while (cap.isOpened()):
    ret,img=cap.read()   ##capturing the image to perform operation on it
    if not ret:
        break;
   
    
    img=np.flip(img,axis=1)
    
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   ##convert the original image RGB to HSV
    
    lower_red=np.array([0,120,70])
    upper_red=np.array([9,255,255])
    
    
    mask1=cv2.inRange(hsv,lower_red,upper_red) ##separate the cloak
    
    lower_red=np.array([171,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)
    
    mask1=mask1+mask2   ##mask1 is the input image
    mask1=cv2.morphologyEx(mask1, cv2.MORPH_OPEN,np.ones((3,3),np.uint8))   ##MORPH_OPEN ERASES THE ALL THE ERRORS OF THE IMAGE
    mask1=cv2.morphologyEx(mask1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8))   ##MORPH_DILATE SMOOTHENS THE IMAGE   AND np.ones() converts image to matrix

    mask2=cv2.bitwise_not(mask1)  ##Except the cloak everything will be  there
    
    
    res1=cv2.bitwise_and(img,img,mask=mask2)  
    res2=cv2.bitwise_and(background,background,mask=mask1)  #### for segmenting the color from the background
    
    finalOutput=cv2.addWeighted(res1,1,res2,1,0) ## add the image and cloak
    ##out.write(finalOutput)
    cv2.imshow("Invisible Cloak",finalOutput)
    h = cv2.waitKey(10)
    if h==27:
        break
    
cap.release()

cv2.destroyAllWindows()