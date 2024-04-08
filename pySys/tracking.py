#!/usr/bin/env python
import cv2
import numpy as np
from blob import Blob
from robot import Robot












def nothing(pos):
	pass
#pre-define
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

x_d=0.0
y_d=0.0
x_d_p=0.0
y_d_p=0.0







distanceThrehold = 50
blobs = []

while(1):
    _, img = cap.read()
    height, width = img.shape[:2]
    #converting frame(img i.e BGR) to HSV (hue-saturation-value)

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    infrared_lower=np.array([0,0,238],np.uint8)
    infrared_upper=np.array([88,255,255],np.uint8)
    infrared=cv2.inRange(hsv,infrared_lower,infrared_upper)
    #Morphological transformation, Dilation  	
    kernal = np.ones((5 ,5), "uint8")
    infrared=cv2.dilate(infrared,kernal)



			
	#Tracking the Blue Color
    (contours,hierarchy)=cv2.findContours(infrared,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)>0:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:
                x, y, w, h = cv2.boundingRect(contour)

                contour_centerX = x + w//2
                contour_centerY = y + h//2
          
                img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                img = cv2.rectangle(img, (0,0),(10,10), (255, 0, 0), 2)
                img = cv2.circle(img, ((2*x+w)//2, (2*y+h)//2), 5, (255, 0, 0), -1)                

                #drawBlob
                img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
                


                x_d = (((2*y+h)/2)-68) * 0.06
                y_d = (((2*x+w)/2)-260) * 0.075
                s = 'x   :'+ str(int(x)) + ' y   :'+ str(int(y))
                cv2.putText(img, s, (x-20, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
              


    cv2.imshow("Mask",infrared)
    cv2.imshow("Color Tracking",img)
    if cv2.waitKey(1)== ord('q'):
        break

cap.release()
cv2.destroyAllWindows()