import numpy as np
from matplotlib import pyplot as plt
import cv2
import math
in_f = open('point_data.txt','r')

datas = []
basic_mul = 0.05

for line in in_f.readlines():
    try:
        line = line[:-1].split(',')
        if float(line[1])==0:
            continue
        else:
            
            datas.append((int(float(line[0])),int(float(line[1]))*basic_mul))
            
    except Exception, e:
        print e
xset=[]
yset=[]
for data in datas:
    theta = data[0]*2*np.pi/360
    x = data[1]*math.cos(-(theta+np.pi/2.0))
    y = data[1]*math.sin(-(theta+np.pi/2.0))
    xset.append(int(x))
    yset.append(int(y))
minn = min(xset)
minn = int(min(yset,minn))
max_num = max(xset)
max_num = int(max(max(yset),max_num))

print len(xset)
in_f.close()


img = np.zeros(((max_num-minn)*1.1,(max_num-minn)*1.1),np.uint8)
for i in xrange(len(xset)):
    img[xset[i]-minn][yset[i]-minn]=255 



lines = cv2.HoughLines(img,1,np.pi/180,1)  

if lines!=None:
    lines1 = lines[:,0,:]
    for rho,theta in lines1[:]: 
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a)) 
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)

cv2.namedWindow("test")
cv2.imshow('test', img) 
print 'end'
print img
cv2.waitKey(0) 
raw_input('ddd')
cv2.destroyWindow("test")






            
