import socket
import time
import sys
import cv2
import numpy as np
import socket
import threading
import random
from robot import Robot
from scene import Scene
import setting as st
import visionAnalyze as va

#Scene Setup:
scene_0 = Scene(510,254,350,150,400,253)
scene_1 = Scene(230,100,350,150,149,230)

#Robots
robot_0 = Robot(0,"192.168.8.218",scene_0)
robot_1 = Robot(1,"192.168.8.215",scene_1)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




#PRE-DEFINE FOR CAMERA

cameraID = 0
video_feed=cv2.VideoCapture(cameraID , cv2.CAP_DSHOW)



#PRE-DEFINE FOR TRACKING
distanceThrehold = 50
areaThrehold     = 200


#functions:
def getVideofeed(videoFeed):
    v,img = videoFeed.read()
    return img



stored_centers = []
missed_centers = []
robots = []

def locationCheck(robots):
     
     for robot in robots:
        robot.lightON(sock)
        robot.walk_forward(sock)
        time.sleep(0.7)
        pre_img  = getVideofeed(video_feed)
        pre_de_noise_img = va.image_denoise(pre_img)
        pre_contours = va.getContours(pre_de_noise_img)
        pre_centers = va.calculate_contour_centers(pre_contours)
        robot.lightOFF(sock)
        time.sleep(0.7)
        post_img  = getVideofeed(video_feed)
        post_de_noise_img = va.image_denoise(post_img)
        post_contours = va.getContours(post_de_noise_img)
        post_centers = va.calculate_contour_centers(post_contours)
        missed_centers = va.find_missing_centers(pre_centers,post_centers)
        if len(missed_centers) != 0:
 
            robot.updateLocation(missed_centers[0][0],missed_centers[0][1])

        else:
           
            pass
        robot.determine_direction()
        robot.lightON(sock)
        #time.sleep(0.3)


threshold = 20

def wandering():
    global robots

    locationCheck(robots)

    for robot in robots:
        robot.new_walk(sock,130)
        time.sleep(0.3)
        robot.walk_by_message(sock,"1")

                            
        
    time.sleep(1)







 

def displayLocations(canvas):
   global robots 

   for robot in robots:

    information = str(robot.id) + " at " + str(robot.locationCenterX) + '-' + str(robot.locationCenterY)
    direction = str(robot.id) + " at " + str(robot.direction)
   
    cv2.putText(canvas, information, (100, 200 * (robot.id+1) ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(canvas, direction, (300, 200 * (robot.id+1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)









locationCheck_thread = None
wander_thread = None

def steup():
    robots.append(robot_0)
    robots.append(robot_1)
    for robot in robots:
         robot.lightON(sock)


def loop():

    global locationCheck_thread


    while(1):

        

        img  = getVideofeed(video_feed)
        de_noise_img = va.image_denoise(img)
               
        if locationCheck_thread is None or not locationCheck_thread.is_alive():
            
            locationCheck_thread = threading.Thread(target=wandering)
            
            locationCheck_thread.start()

        img_res = cv2.resize(img,(640,480))
        de_img_res = cv2.resize(de_noise_img,(640,480))
        de_img_3channel = cv2.cvtColor(de_img_res, cv2.COLOR_GRAY2BGR)
        canvas = np.zeros((st.canvas_height,st.canvas_width,3), dtype=np.uint8)
        canvas[0:480,0:640] = img_res
        canvas[0:480,640:1280] = de_img_3channel

        displayLocations(canvas)

        cv2.imshow('w1',canvas)
    
    


        
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'):
            break
        
 





if __name__ == '__main__':
    steup()
    loop()



    
 