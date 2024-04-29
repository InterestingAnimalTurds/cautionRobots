import socket
import time
import sys
import cv2
import numpy as np
import socket
import threading
import random
import math
from robot import Robot
from scene import Scene
import setting as st
import visionAnalyze as va

#Scene Setup:
scene_0 = Scene(386,329,70)
scene_1 = Scene(143,319,70)
scene_2 = Scene(386,100,70)
scene_3 = Scene(130,100,70)

#Robots
robot_0 = Robot(0,"192.168.8.218",scene_0)
robot_1 = Robot(1,"192.168.8.215",scene_1)
robot_2 = Robot(2,"192.168.8.125",scene_2)
robot_3 = Robot(3,"192.168.8.210",scene_3)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#PRE-DEFINE FOR CAMERA

cameraID = 0
video_feed=cv2.VideoCapture(cameraID , cv2.CAP_DSHOW)

pts1 = np.float32([[93, 64], [77, 376], [553, 54], [523, 435]])
# 目标点坐标
pts2 = np.float32([[93, 64], [93,376], [553, 64], [553, 376]])


Pmatrix = cv2.getPerspectiveTransform(pts1, pts2)

#PRE-DEFINE FOR TRACKING
distanceThrehold = 50
areaThrehold     = 200


#functions:
def getVideofeed(videoFeed):
    v,img = videoFeed.read()
    return img

hihi_threhold = 50

stored_centers = []
missed_centers = []
robots = []

def locationCheck(robots):
     
     random.shuffle(robots)
     for robot in robots:
        print(f"This is Robot ID : {robot.id}")
        robot.lightON(sock)
        #robot.walk_forward(sock)
        time.sleep(0.2)
        pre_img  = getVideofeed(video_feed)
        pre_de_noise_img = va.image_denoise(pre_img)
        pre_contours = va.getContours(pre_de_noise_img)
        pre_centers = va.calculate_contour_centers(pre_contours)
        robot.lightOFF(sock)
        time.sleep(0.2)
        post_img  = getVideofeed(video_feed)
        #post_img  = cv2.warpPerspective(post_img, Pmatrix, (720,720 ))
        post_de_noise_img = va.image_denoise(post_img)
        post_contours = va.getContours(post_de_noise_img)
        post_centers = va.calculate_contour_centers(post_contours)
        missed_centers = va.find_missing_centers(pre_centers,post_centers)
        print(missed_centers)
        if len(missed_centers) != 0: 
            robot.updateLocation(missed_centers[0][0],missed_centers[0][1])
        else:
            pass
        robot.lightON(sock)
        missed_centers = []
        time.sleep(0.1)
        robot.walk_by_message(sock,"1")


def directionCheck(robots):
    random.shuffle(robots)
    for robot in robots:
        print(f"This is Robot ID : {robot.id}")
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
        #post_img  = cv2.warpPerspective(post_img, Pmatrix, (720,720 ))
        post_de_noise_img = va.image_denoise(post_img)
        post_contours = va.getContours(post_de_noise_img)
        post_centers = va.calculate_contour_centers(post_contours)
        missed_centers = va.find_missing_centers(pre_centers,post_centers)
        print(missed_centers)
        if len(missed_centers) != 0: 
            robot.updateDIRLocation(missed_centers[0][0],missed_centers[0][1])
        else:
            pass
        robot.determine_direction()
        robot.lightON(sock)
        missed_centers = []
        time.sleep(0.2)

threshold = 50

def wandering():
    global robots

    
    locationCheck(robots)
   
    directionCheck(robots)

    for robot in robots:
        robot.new_walk(sock,hihi_threhold)
        #robot.walk_by_message(sock,"1")
        random_delay = random.uniform(0.2, 2)
        time.sleep(random_delay)
     
 




def displayLocations(canvas):
   global robots 

   for robot in robots:
    information = str(robot.id) + " at " + str(robot.locationCenterX) + '-' + str(robot.locationCenterY)
    direction = str(robot.id) + " at " + str(robot.direction)
   
    cv2.putText(canvas, information, (100, 100 * (robot.id+1) ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(canvas, direction, (300, 100 * (robot.id+1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)









locationCheck_thread = None
wander_thread = None

def steup():
    robots.append(robot_0)
    robots.append(robot_1)
    robots.append(robot_2)
    robots.append(robot_3)
    for robot in robots:
         robot.lightON(sock)


def loop():

    global locationCheck_thread
    global img

    while(1):

        

        img  = getVideofeed(video_feed)
        #img  = cv2.warpPerspective(img, Pmatrix, (640,480 ))
        de_noise_img = va.image_denoise(img)
               
        if locationCheck_thread is None or not locationCheck_thread.is_alive():
            
            locationCheck_thread = threading.Thread(target=wandering)
            
            locationCheck_thread.start()



        cv2.circle(img, (scene_0.centerX,scene_0.centerY), scene_0.radius, (255,0,0), 1)        
        cv2.circle(img, (scene_1.centerX,scene_1.centerY), scene_1.radius, (255,0,0), 1)        
        cv2.circle(img, (scene_2.centerX,scene_2.centerY), scene_2.radius, (255,0,0), 1)        
        cv2.circle(img, (scene_3.centerX,scene_3.centerY), scene_3.radius, (255,0,0), 1)        

        cv2.circle(img, (scene_0.centerX,scene_0.centerY), scene_0.radius - hihi_threhold, (0,0,255), 1)        
        cv2.circle(img, (scene_1.centerX,scene_1.centerY), scene_1.radius - hihi_threhold, (0,0,255), 1)        
        cv2.circle(img, (scene_2.centerX,scene_2.centerY), scene_2.radius - hihi_threhold, (0,0,255), 1)        
        cv2.circle(img, (scene_3.centerX,scene_3.centerY), scene_3.radius - hihi_threhold, (0,0,255), 1)        


        for robot in robots:
            len = 100
            end_x = int(robot.locationCenterX + len * math.cos(math.radians(robot.direction)))
            end_y = int(robot.locationCenterY + len * math.sin(math.radians(robot.direction)))
            cv2.line(img, (robot.locationCenterX,robot.locationCenterY),(end_x,end_y) , (0,255,0), 1)
            cv2.circle(img,(end_x,end_y),(5),(0,255,0), 2)
            cv2.circle(img,(robot.pre_locationCenterX,robot.pre_locationCenterY),(5),(0,255,255), 2)
            cv2.circle(img,(robot.locationCenterX,robot.locationCenterY),(5),(255,255,0), 2)

            cv2.line(img,(robot.pre_locationCenterX,robot.pre_locationCenterY),(robot.scene.centerX,robot.scene.centerY),(255,255,255),1)

 
   
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



    
 