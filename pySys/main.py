import socket
import time
import sys
import cv2
import numpy as np
import socket
import threading
import random
from robot import Robot
#Canvas 
canvas_height = 480*2 + 100
canvas_width = 640*2 + 100





#first Robot
robot_0 = Robot(0,"192.168.8.218")
robot_1 = Robot(1,"192.168.8.215")

#need to test async


#PRE-DEFINE FOR NETWORK
esp32_ip = "192.168.8.218"
esp32_port = 5555


# esp32_ip = "127.0.0.1"
# esp32_port = 9911
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
esp32_addr = (esp32_ip,esp32_port)


#PRE-DEFINE For Robot
robotPort = 5555





#PRE-DEFINE FOR CAMERA

cameraID = 0
video_feed=cv2.VideoCapture(cameraID , cv2.CAP_DSHOW)

LH = 0
LS = 0
LV = 238
UH = 88
US = 255
UV = 255
lower_HSV = np.array([LH,LS,LV],np.uint8)
upper_HSV = np.array([UH,US,UV],np.uint8)




#PRE-DEFINE FOR TRACKING
distanceThrehold = 50
areaThrehold     = 200


#functions:
def getVideofeed(videoFeed):
    v,img = videoFeed.read()
    return img


def image_denoise(img):

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    infrared=cv2.inRange(hsv,lower_HSV,upper_HSV)
    #Morphological transformation, Dilation  	
    kernal = np.ones((5 ,5), "uint8")
    de_img=cv2.dilate(infrared,kernal)
    return de_img

def getContours(img):
    (contours,hierarchy)=cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours




def calculate_contour_centers(contours):
    centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M['m00'] != 0:
            centerX = int(M['m10'] / M['m00'])
            centerY = int(M['m01'] / M['m00'])
            centers.append((centerX, centerY))
    return centers

def find_missing_centers(pre_centers, post_centers, threshold=20):
    miss_centers = []
  
    for pre_center in pre_centers:
        found = False
        if len(post_centers) == 0:
             print("lenth0")
             miss_centers.append(pre_centers)

        else:
            for post_center in post_centers:
                distance = np.sqrt((pre_center[0] - post_center[0]) ** 2 + (pre_center[1] - post_center[1]) ** 2)
                if distance < threshold:
                    found = True
                    break  
                if not found:
                    miss_centers.append(pre_center)
    return miss_centers




def keyLogic(key):
    global robots

    if key == ord('r'):  # 如果按下's'键，则打印信息
            message = 'LED1'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('e'):  # 如果按下's'键，则打印信息
            message = 'LED0'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('s'):  # 如果按下's'键，则打印信息
            #message = 'FORWARD'
            for robot in robots:
                robot.walk(sock)
            #print(f"Sending: {message}")
            #sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('w'):  # 如果按下's'键，则打印信息
            message = 'FORWARD'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('a'):  # 如果按下's'键，则打印信息
            message = 'LEFT'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('d'):  # 如果按下's'键，则打印信息
            message = 'RIGHT'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('o'):  # 如果按下's'键，则打印信息
            message = '1'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)








stored_centers = []
missed_centers = []




robots = []

def locationCheck(robots):
   
  
     
     for robot in robots:
        robot.lightON(sock)
        robot.walk_forward(sock)
        time.sleep(1)
        pre_img  = getVideofeed(video_feed)
        pre_de_noise_img = image_denoise(pre_img)
        pre_contours = getContours(pre_de_noise_img)
        pre_centers = calculate_contour_centers(pre_contours)
        robot.lightOFF(sock)
        time.sleep(0.2)
        post_img  = getVideofeed(video_feed)
        post_de_noise_img = image_denoise(post_img)
        post_contours = getContours(post_de_noise_img)
        post_centers = calculate_contour_centers(post_contours)
        missed_centers = find_missing_centers(pre_centers,post_centers)
        if len(missed_centers) != 0:
            print(missed_centers[0][0])
            robot.updateLocation(missed_centers[0][0][0],missed_centers[0][0][1])
        else:
            pass
        robot.determine_direction()
        robot.lightON(sock)
        #time.sleep(0.3)
   
# boardminX = 31
# boardmaxX = 510
# boardminY = 118
# boardmaxY = 400
# threshold = 20
#510 - 400
#31 118
def wandering():
    global robots
    boardminX = 131
    boardmaxX = 510
    boardminY = 118
    boardmaxY = 400
    threhold = 80
    locationCheck(robots)

    for robot in robots:
        robot.walk(sock,boardmaxX,boardminX,boardmaxY,boardminY,threhold,270, 238)
    time.sleep(2)







 

def displayLocations(canvas):
   global robots 

   for robot in robots:

    information = str(robot.id) + " at " + str(robot.locationCenterX) + '-' + str(robot.locationCenterY)
    direction = str(robot.id) + " at " + str(robot.direction)
   
    cv2.putText(canvas, information, (100, 200 * (robot.id+1) ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(canvas, direction, (300, 200 * (robot.id+1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
     # cv2.putText(canvas, information, (100, 200 * (robot.id+1) ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)








locationCheck_thread = None
wander_thread = None

def steup():
    robots.append(robot_0)
    robots.append(robot_1)

#510 - 400
#31 118
def loop():

    global locationCheck_thread
    global wander_thread

    while(1):

        

        img  = getVideofeed(video_feed)

        de_noise_img = image_denoise(img)
       
        
        if locationCheck_thread is None or not locationCheck_thread.is_alive():
            
            locationCheck_thread = threading.Thread(target=wandering)
            
            locationCheck_thread.start()


        img_res = cv2.resize(img,(640,480))
        de_img_res = cv2.resize(de_noise_img,(640,480))
        de_img_3channel = cv2.cvtColor(de_img_res, cv2.COLOR_GRAY2BGR)
        canvas = np.zeros((canvas_height,canvas_width,3), dtype=np.uint8)
        canvas[0:480,0:640] = img_res
        canvas[0:480,640:1280] = de_img_3channel

        displayLocations(canvas)

        cv2.imshow('w1',canvas)

    


        
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'):
            break
        
        keyLogic(key)

 





if __name__ == '__main__':
    steup()
    loop()



    
 