import socket
import time
import sys
import cv2
import numpy as np
import socket

#Canvas 
canvas_height = 480*2 + 100
canvas_width = 640*2 + 100








#need to test async




#PRE-DEFINE FOR NETWORK
# esp32_ip = "192.168.8.218"
# esp32_port = 5555


esp32_ip = "127.0.0.1"
esp32_port = 9911
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
esp32_addr = (esp32_ip,esp32_port)


#PRE-DEFINE For Robot
robotPort = 5555

robot_0_ip = "0.0.0.0"
robot_1_ip = "0.0.0.0"
robot_2_ip = "0.0.0.0"
robot_3_ip = "0.0.0.0"

robot_0_id = 0
robot_0_id = 1
robot_0_id = 2
robot_0_id = 3




#PRE-DEFINE FOR CAMERA

cameraID = 1
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

def findRobotPosition():
    #get Contorus
    #Turn off the Light
    #get Contorus
    #check which one gone
    #assign position
    pass

def keyLogic(key):
    if key == ord('r'):  # 如果按下's'键，则打印信息
            message = 'LED1'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('e'):  # 如果按下's'键，则打印信息
            message = 'LED0'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
    elif key == ord('s'):  # 如果按下's'键，则打印信息
            message = 'FORWARD'
            print(f"Sending: {message}")
            sent = sock.sendto(message.encode(), esp32_addr)
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




def BoarderCheck():
    #check every position of robot
    #if one position close:
    #turn around
    pass 
def HitCheck():
    #check all the position of robot;
    #if one position close:
    #one turn right one turn left
    pass


def wandering():
    pass

def drawContours(contours,_img):
          if len(contours)>0:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 200:
                    x, y, w, h = cv2.boundingRect(contour)
                

                    contour_centerX = x + w//2
                    contour_centerY = y + h//2
            
                    _img = cv2.rectangle(_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    _img = cv2.rectangle(_img, (0,0),(10,10), (0, 0, 255), 2)
                    _img = cv2.circle(_img, ((2*x+w)//2, (2*y+h)//2), 5, (255, 0, 0), -1)                

                    #drawBlob
                    _img = cv2.rectangle(_img, (x, y), (x+w, y+h), (255, 255, 0), 2)
                    return 1
             
            else:
               return 0
        

# def setup():

  #location Alghorim:

# store one state of locations:
# def store_location(array_contors):
#     someArray_1 = array_contors;
#     return someArray_1

# def check_different(array_contors):
#     #centorPoint

#     #check every one 


#points = [] 

previous_contours = None





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
    missing_centers = []
    for pre_center in pre_centers:
        found = False
        for post_center in post_centers:
            distance = np.sqrt((pre_center[0] - post_center[0]) ** 2 + (pre_center[1] - post_center[1]) ** 2)
            if distance < threshold:
                found = True
                break  # 如果找到匹配，则标记为found并跳出内循环
            if not found:
                missing_centers.append(pre_center)
                 

    return missing_centers


offStartTime = 0
onStartTime = 0
waitTime = 0.5
ledState = 'OFF'  # 初始LED状态为关闭



        
def blinkLED():

    global offStartTime, onStartTime, waitTime, ledState
    currentTime = time.time()

    if ledState == 'OFF' and (offStartTime == 0 or currentTime - offStartTime > waitTime):
        message = 'LED1'
        sent = sock.sendto(message.encode(), esp32_addr)
        ledState = 'ON'
        onStartTime = currentTime
        offStartTime = 0
   

    elif ledState == 'ON' and (onStartTime == 0 or currentTime - onStartTime > waitTime):
        message = 'LED0'
        sent = sock.sendto(message.encode(), esp32_addr)
        ledState = 'OFF'
        offStartTime = currentTime
        onStartTime = 0
        checked = 0
      



         
         
  


     

# def get_location(pre_contours,de_noise_img,startTime,waitTime):
#     pre_centers = calculate_contour_centers(pre_contours)
#     if startTime == 0:
#         message = 'LED0'
#         sent = sock.sendto(message.encode(), esp32_addr)
#         startTime = time.time()
#     else:
#         if time.time() - startTime < waitTime:
#             post_contours = getContours(de_noise_img)
#             post_centers = calculate_contour_centers(post_contours)
#             missing_centers = find_missing_centers(pre_centers, post_centers)
        
#             if len(missing_centers) == 1:
#                 startTime = 0
#                 message = 'LED1'
#                 sent = sock.sendto(message.encode(), esp32_addr)
#                 return f"location is {missing_centers[0]}"
#             else:
#                 message = 'LED1'
#                 sent = sock.sendto(message.encode(), esp32_addr)
#                 startTime = 0
#                 return f"multiple found or None"


def turnOffLight():
    message = 'LED0'
    sent = sock.sendto(message.encode(), esp32_addr)
def turnONLight():
    message = 'LED1'
    sent = sock.sendto(message.encode(), esp32_addr)

stored_centers = []
missed_centers = []

def loop():


    while(1):
        img  = getVideofeed(video_feed)

        de_noise_img = image_denoise(img)
        contours = getContours(de_noise_img)
        stored_centers = calculate_contour_centers(contours)
        turnOffLight()
        time.sleep(0.5)
        contours = getContours(de_noise_img)
        missed_centers = find_missing_centers(stored_centers, calculate_contour_centers(contours))
        turnONLight()
        


        # drawed_img = drawContours(contours,img)
        # previous_contours = contours
        # #blinkLED()



        img_res = cv2.resize(img,(640,480))

        de_img_res = cv2.resize(de_noise_img,(640,480))
        de_img_3channel = cv2.cvtColor(de_img_res, cv2.COLOR_GRAY2BGR)
        canvas = np.zeros((canvas_height,canvas_width,3), dtype=np.uint8)

        canvas[0:480,0:640] = img_res
        canvas[0:480,640:1280] = de_img_3channel
        
        cv2.putText(canvas, str(S), (100-20, 200-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        
        cv2.imshow('w1',canvas)

        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'):
            break
        keyLogic(key)





if __name__ == '__main__':
    loop()


# #    while True:
#         img = getVideofeed(video_feed)
#         de_noise_img = image_denoise(img)
#         contours = getContours(de_noise_img)
#         stored_centers = calculate_contour_centers(contours)

#         # 创建一个线程来处理LED关闭、等待、检测轮廓的逻辑
#         thread = threading.Thread(target=process_led_and_contours, args=(de_noise_img, stored_centers))
#         thread.start()

#         # 继续你的主循环其他任务...
#         img_res = cv2.resize(img, (640, 480))
#         de_img_res = cv2.resize(de_noise_img, (640, 480))
#         de_img_3channel = cv2.cvtColor(de_img_res, cv2.COLOR_GRAY2BGR)
#         canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

#         canvas[0:480, 0:640] = img_res
#         canvas[0:480, 640:1280] = de_img_3channel
        
#         # 绘制文本、显示画布等
#         cv2.imshow('w1', canvas)

#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):
#             break
#         keyLogic(key)
    


#     #thread = threading.Thread(target=process_led_and_contours, args=(de_noise_img, stored_centers))
# thread.start()
# thread.join() 