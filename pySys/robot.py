import socket
import numpy as np
import random
import utilties as ut
import scene as sc
class Robot:
    
    def __init__(self, _id,_ip,_robotscene,_port = 5555, ):
        self.id = _id
        
        self.ip = _ip
        
        self.port = _port
        
        self.addr = (self.ip,self.port)

        self.locationCenterX = 0
        self.locationCenterY = 0

        self.pre_locationCenterX = 0
        self.pre_locationCenterY = 0

        self.direction = 0
        self.boarderCheckFlag = False

        self.inTurningCounts = 0
        self.leavingCounts = 0
        self.scene = _robotscene



        self.backward = 0

    def updateLocation(self,centerX,centerY):
        
        if self.locationCenterX != centerX or self.locationCenterY != centerY :        
            self.pre_locationCenterX = self.locationCenterX
            self.pre_locationCenterY = self.locationCenterY
        self.locationCenterX = centerX
        self.locationCenterY = centerY
        



    def lightOFF(self,sock):
        message = 'LED0'
        sent = sock.sendto(message.encode(), self.addr)
    def lightON(self,sock):
        message = 'LED1'
        sent = sock.sendto(message.encode(), self.addr)





    def new_walk(self,sock,threhold):

        message = self.in_range_circle(threhold)
        sent = sock.sendto(message.encode(), self.addr)




    def walk_by_message(self,sock,message):
        msg = message
        sent = sock.sendto(message.encode(),self.addr)


    def walk_forward(self,sock):
        message = "FORWARD"
        sent = sock.sendto(message.encode(),self.addr)



        
  

    
    def determine_direction(self):  
        delta_x = self.locationCenterX - self.pre_locationCenterX
        delta_y = self.locationCenterY - self.pre_locationCenterY
        direction = (delta_x,delta_y)
        angle_radians = np.arctan2(delta_y, delta_x)
        angle_degrees = np.degrees(angle_radians)
        self.direction  =  angle_degrees










            
    def move_to_center(self,centerX,centerY):
    # 假设中心点坐标为 centerX, centerY
        delta_x = centerX - self.locationCenterX
        delta_y = centerY - self.locationCenterY
        angle_radians = np.arctan2(delta_y, delta_x)
        angle_degrees = np.degrees(angle_radians)
        self.direction = angle_degrees



    def boarderCheck(self,threhold):
        mDistanceX = self.scene.MAXWIDTH  - self.locationCenterX
        MDistanceX = self.locationCenterX - self.scene.MINWIDTH
        MDistanceY = self.locationCenterY - self.scene.MAXHEIGHT
        mDistanceY = self.scene.MINHEIGHT - self.locationCenterY 
        
        if mDistanceX < threhold or MDistanceX < threhold or MDistanceY < threhold or mDistanceY < threhold:


            if mDistanceX < threhold:  # Near the right border
                targetX = self.scene.MINWIDTH  # Set target to the left side
            elif MDistanceX < threhold:  # Near the left border
                targetX = self.scene.MAXWIDTH  # Set target to the right side
            else:
                targetX = self.locationCenterX  # Stay in the current horizontal position

            if mDistanceY < threhold:  # Near the top border
                targetY = self.scene.MINHEIGHT  # Set target to the bottom side
            elif MDistanceY < threhold:  # Near the bottom border
                targetY = self.scene.MAXHEIGHT  # Set target to the top side
            else:
                targetY = self.locationCenterY 
            
            if self.inTurningCounts == 0:

                delta_x = targetX - self.locationCenterX
                delta_y = targetY - self.locationCenterY
                angle_radians = np.arctan2(delta_y, delta_x)
                self.targetDirection = np.degrees(angle_radians)
                self.targetDirection = (self.targetDirection + 360) % 360  # 确保方向在0到360度之间
                print(f"Target Direction: {self.targetDirection}")

            currentDirection = (self.direction + 360) % 360
            directionDifference = ut.calculate_angle_difference(self.targetDirection, currentDirection)

            print(f"Current Direction: {currentDirection}, Difference: {directionDifference}")

            # 如果方向差距大于一定阈值（比如10度），继续转向
            if abs(directionDifference) > 90:
                self.inTurningCounts += 1
                return "LEFT"
            else:
                # 方向差距足够小，可以直行
                self.inTurningCounts = 0
              
                return "FORWARD"
        else:
            message = random.choice(["FORWARD","1"])
            return message
        
    

    def in_range_circle(self,threshold):
        centerX = self.scene.centerX
        centerY = self.scene.centerY
        radius = self.scene.radius

        distance_to_center = np.sqrt((self.locationCenterX - centerX)**2 + (self.locationCenterY - centerY)**2)
        
        if distance_to_center > radius - threshold:
            
            delta_x = centerX - self.locationCenterX
            delta_y = centerY - self.locationCenterY
            angle_radians = np.arctan2(delta_y, delta_x)
            self.targetDirection = np.degrees(angle_radians)
            self.targetDirection = (self.targetDirection + 360) % 360

            currentDirection = (self.direction + 360) % 360
            directionDifference = ut.calculate_angle_difference(self.targetDirection, currentDirection)
            print(f"Current Direction: {currentDirection}, Difference: {directionDifference}")

            if abs(directionDifference) > 60:
                self.inTurningCounts += 1
                return "LEFT"  
            else:
                # 方向差距足够小，可以直行
                self.inTurningCounts = 0
                return "FORWARD"
            
        else:
            return "FORWARD"


        
#Utilitys:
    
