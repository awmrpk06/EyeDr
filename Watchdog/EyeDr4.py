import cv2
import sys
import numpy as np
import csv
import pandas as pd
import os
import re
import string_split as js
csv_name = 'DATA_26062022.csv'
w_process = 640
h_process = 480
index = 0
aD = 166.14221331019428; bD = -1.8433900167479054; cD = 0.01009104294584857; dD = -2.7251091520976264e-05; eD = 2.9073925247676148e-08; fD = -5790.1772194276555
aC = 121.72160706808744; bC = -1.4072184730873407; cC = 0.008008623073192875; dC = -2.23687581598597e-05; eC = 2.4568387357272637e-08; fC = -4020.175253867087
def nothing(x):
    pass
def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
def ReadImg():
   # get the path/directory
    folder_dir = 'TRAININGSET/'
    # count = 1292
    files = os.listdir(folder_dir)
    files = sorted(files, key=numericalSort)
    for images in files:
      #  print("iterindex: ",count.counter)
      #  print(files[count.counter])
        print(images)
        img = cv2.imread(folder_dir + images)
        height, width, channels = img.shape
        result =  EyeDr(name,img, height, width)
        cv2.imwrite(os.path.join('Labeled_GLC/' , images), result)
def removearray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind],arr):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')
def getContours (org_img,cThr=[50,100],minArea = 0, filter = 4,showCanny = False,draw = False):
    img = org_img.copy()
   # imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(img,cThr[0],cThr[1])
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    if showCanny : cv2.imshow('Canny',imgThre)
    contours,hiearchy = cv2.findContours(imgThre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []
    for i in contours:
        peri = cv2.arcLength(i,True)
        approx = cv2.approxPolyDP(i,0.02*peri,True)
        area = cv2.contourArea(i)
        if area > minArea:
            finalContours.append(i)
    return img,finalContours
def Filter(image, thres, value, maxVal):
    imgEye = image.copy()
    mask_img = cv2.inRange(imgEye, value ,maxVal)
  #  cv2.imshow("Mask: " + str(value) ,mask_img)
    img_d, contours = getContours(org_img = mask_img, showCanny = False)
    finalContours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        finalContours.append([area, cnt])
      #  cv2.polylines(image, cnt, 1, (255,0,0))
    finalContours = sorted(finalContours,key = lambda x:x[0],reverse = True)
    if (finalContours):
        (x,y,w,h) = cv2.boundingRect(finalContours[0][1])
    else:
        (x,y,w,h) = (0,0,0,0)
    return x,y,w,h
def FindBrightestP(image, thres):
    imgEye = image.copy()
    gray = cv2.cvtColor(imgEye, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (thres, thres), 0)
    kernel = np.ones((thres,thres))
    #imgDial = cv2.dilate(gray,kernel,iterations = 2)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # cv2.imshow("grayscale",bright)
    print("Brightest point: ", maxVal)
    return gray, maxVal
def EyeDr(name,image, height, width ,thresD = 7, thresC = 7):
    imgEye = image.copy()
    mask_img, maxVal = FindBrightestP(imgEye, thresD)
    #cv2.imshow("Mask: ",mask_img)
    vCup = int(objective(maxVal, aC, bC, cC, dC, eC, fC))
    vDisc = int(objective(maxVal, aD, bD, cD, dD, eD, fD))
    print("vCup :%d, vDisc :%d"%(vCup, vDisc))
    (x_c, y_c, w_c, h_c) = Filter(mask_img ,thresC, vCup, maxVal)
    (x_d, y_d, w_d, h_d) = Filter(mask_img ,thresD, vDisc, maxVal)

    print("width: %d, height: %d"%(width,height))
    eye = js.getEye(name)
    (s,t,n,i) = SNTI(eye,imgEye, x_c, y_c, x_d, y_d, w_c, h_c, w_d, h_d)
    
    print("Cup:  x:%f, y: %f, w:%f, h:%f "%(x_c/width + w_c/(width*2) , y_c/height + h_c/(height*2), w_c/width ,h_c/height))
    print("Disc:  x:%f, y: %f, w:%f, h:%f "%(x_d/width + w_d/(width*2), y_d/height + h_d/(height*2) ,w_d/width ,h_d/height))
   # WriteToCSV(count, name, s, n, t, i, x_c, y_c, w_c, h_c, x_d, y_d, w_d, h_d)
   
    return (imgEye,s, n, t, i, x_c/width + w_c/(width*2) , y_c/height + h_c/(height*2) , w_c/width, h_c/height,
            x_d/width + w_d/(width*2), y_d/height + h_d/(height*2), w_d/width, h_d/height)
def returnToOrginalSize(x_c, y_c, x_d, y_d, w_c, h_c, w_d, h_d, height, width):
    x_c = int(float(x_c/w_process)*width)
    y_c = int(float(y_c/h_process)*height)
    w_c = int(float(w_c/w_process)*width)
    h_c = int(float(h_c/h_process)*height)
              
    x_d = int(float(x_d/w_process)*width)
    y_d = int(float(y_d/h_process)*height)
    w_d = int(float(w_d/w_process)*width)
    h_d = int(float(h_d/h_process)*height)
    return x_c, y_c, x_d, y_d, w_c, h_c, w_d, h_d
def SNTI(eye ,img ,x_c,y_c ,x_d, y_d, w_c, h_c, w_d, h_d):
    s = y_c - y_d 
    t = x_c - x_d
    n = x_d + w_d - x_c - w_c 
    i = y_d + h_d - y_c - h_c
    cv2.line(img, (x_d + int(w_d/2), y_d), (x_d + int(w_d/2), y_c), (255,0,0), 3)
    cv2.line(img, (x_d, y_d + int(h_d/2)), (x_c, y_d + int(h_d/2)), (255,0,0), 3)
    cv2.line(img, (x_c + w_c, y_d + int(h_d/2)), (x_d + w_d, y_d + int(h_d/2)), (255,0,0), 3)
    cv2.line(img, (x_d + int(w_d/2), y_d + h_d), (x_d + int(w_d/2), y_c + h_c), (255,0,0), 3)
    cv2.putText(img, "I", ( x_d + int(w_d/2), y_d + int(h_d*1.5) ), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0), 3)
    cv2.putText(img, "S", ( x_d + int(w_d/2), y_d - int(h_d/6) ), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0), 3)
    if eye == "L":
        n, t = t, n
        cv2.putText(img, "N", ( x_d - int(w_d/3), y_d + int(h_d/2) ), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0), 3)
        cv2.putText(img, "T", ( x_c + int(w_c*1.25),  y_d + int(h_d/2) ), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0), 3)
    else:
        cv2.putText(img, "T", ( x_d - int(w_d/4), y_d + int(h_d/2) ), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0), 3)
        cv2.putText(img, "N", ( x_c + int(w_c*1.25),  y_d + int(h_d/2) ), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0), 3) 
    cv2.rectangle(img, (x_d, y_d), (x_d + w_d, y_d + h_d), (255, 255, 255), 3)
    cv2.rectangle(img, (x_c, y_c), (x_c + w_c, y_c + h_c), (0, 255, 0), 3)
    print("s = %d, t = %d, n = %d, i = %d" %(s,t,n,i))
    return s,t,n,i
def objective(x, a, b, c, d, e, f):
	return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f

    
#ReadImg()
