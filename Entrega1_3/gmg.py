#!/usr/bin/env python
import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture('video.wmv')
ret, originalFrame = cap.read()

 
while(1):
    ret, frame = cap.read()
    finalImg = frame

    #Current
    cv2.imshow('Real video',frame)

    #Current en GreyScale
    currGreyImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Current Grey Scale Image', currGreyImg)

    #Reference Grey Image
    refGreyImg = cv2.cvtColor(originalFrame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Reference Grey Image', refGreyImg)

    #Absolute Difference Image
    diff = cv2.absdiff(currGreyImg, refGreyImg)
    cv2.imshow('Absolute Difference Image', diff)

    #Thresholding Difference Image
    blurred = cv2.GaussianBlur(diff, (5, 5), 0)
    thImg = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('Threshold Image', thImg)

    #Centroid Image
    cnts = cv2.findContours(thImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if(len(cnts)!=0):
        c = max(cnts, key = cv2.contourArea)
    #for c in cnts:
        M = cv2.moments(c)
        cX = int(M["m10"] / (M["m00"]+0.00005))
        cY = int(M["m01"] / (M["m00"]+0.00005))
        cv2.drawContours(finalImg, [c], -1, (0, 255, 0), 2)
        cv2.circle(finalImg, (cX, cY), 7, (255, 255, 255), -1)
 
	    # draw the contour and center of the shape on the image
        cv2.drawContours(finalImg, [c], -1, (0, 255, 0), 2)
        cv2.circle(finalImg, (cX, cY), 7, (0, 0, 255), -1)
    cv2.imshow('Centroide', finalImg)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
 
cap.release()
cv2.destroyAllWindows()