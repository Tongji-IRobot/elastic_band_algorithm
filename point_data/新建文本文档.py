# -*- coding: cp936 -*-
import cv2
import numpy as np
import cv2.cv as cv
cv2.namedWindow("test")#命名一个窗口
cv2.namedWindow("canny")#命名一个窗口
cap=cv2.VideoCapture(0)#打开1号摄像头

success, frame = cap.read()#读取一桢图像，前一个返回值是是否成功，后一个返回值是图像本身
res = {}

while success:
    success, frame = cap.read()
    img = frame

    img = cv2.GaussianBlur(img,(3,3),0)  
    edges = cv2.Canny(img, 50, 150, apertureSize = 3)  
    lines = cv2.HoughLines(edges,1,np.pi/180,118)  
    result = img.copy()  
    
    #经验参数  
    minLineLength = 200  
    maxLineGap = 15  
    lines = cv2.HoughLinesP(edges,1,np.pi/180,80,minLineLength,maxLineGap)  
    for x1,y1,x2,y2 in lines[0]:  
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)


    cv2.imshow('test', img) 

    key=cv2.waitKey(10)
    c = chr(key & 255)
    if c in ['q', 'Q', chr(27)]:
        break
raw_input('ddd')
cv2.destroyWindow("test")
