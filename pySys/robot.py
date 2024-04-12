import socket
import numpy as np
import random
class Robot:
    


    def __init__(self, _id,_ip,_port = 5555):
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



    def updateLocation(self,centerX,centerY):
        
        if self.locationCenterX != centerX or self.locationCenterY != centerY :
            
            self.pre_locationCenterX = self.locationCenterX
            self.pre_locationCenterY = self.locationCenterY


        self.locationCenterX = centerX
        self.locationCenterY = centerY
        
        print(f"preX = {self.pre_locationCenterX}")
        print(f"preY = {self.pre_locationCenterY}")
        print(f"NOW = {self.locationCenterX}")
        print(f"NOW = {self.locationCenterY}")


    def lightOFF(self,sock):
        message = 'LED0'
        sent = sock.sendto(message.encode(), self.addr)
    
    def lightON(self,sock):
        message = 'LED1'
        sent = sock.sendto(message.encode(), self.addr)

    def walk(self,sock,boardmaxX,boardminX,boardmaxY,boardminY,threhold,centerX,centerY):

        message = self.boarderCheck(boardmaxX,boardminX,boardmaxY,boardminY,threhold,centerX,centerY)
        sent = sock.sendto(message.encode(), self.addr)

  
    def walk_forward(self,sock):
        message = "FORWARD"
        sent = sock.sendto(message.encode(),self.addr)

    def calculate_angle_difference(self,target_angle, current_angle):
        difference = (target_angle - current_angle + 180) % 360 - 180
        return difference

    #     pass
    # def boarderCheck(self,boardmaxX,threhold):
    #     mDistanceX =  boardmaxX - self.locationCenterX 
    #     if mDistanceX < threhold:
    #         print("HIT!")
    #         self.inTurningCounts += 1
    #         if self.inTurningCounts == 1:
    #             self.targetDirection = (self.direction + 180) % 360
    #             print(f"targetD = {self.targetDirection}")
    #         else:
    #             pass
    #         turningDirection = self.calculate_angle_difference(self.targetDirection,self.direction)
    #         if abs(turningDirection) <= 40 and self.leavingCounts <= 4:
    #             print(f"turningDirection = {turningDirection}")
    #             print(f"leavingCounts = {self.leavingCounts}")
    #             self.leavingCounts += 1
    #             self.inTurningCounts = 0
    #             return "FORWARD"
    #         else:
    #             return "LEFT"
                 
    #     else:
    #         self.leavingCounts = 0
    #         return "FORWARD"
        
    def boarderCheck(self, boardmaxX,boardminX,boardmaxY,boardminY,threshold,centerX,centerY):
        mDistanceX = boardmaxX - self.locationCenterX
        MDistanceX = self.locationCenterX - boardminX 
        MDistanceY = self.locationCenterY - boardminY
        mDistanceY = boardmaxY - self.locationCenterY 
        
    

        if mDistanceX < threshold or MDistanceX < threshold or MDistanceY < threshold or mDistanceY < threshold:
            if self.inTurningCounts == 0:
                delta_x = centerX - self.locationCenterX
                delta_y = centerY - self.locationCenterY
                angle_radians = np.arctan2(delta_y, delta_x)
                self.targetDirection = np.degrees(angle_radians)
                self.targetDirection = (self.targetDirection + 360) % 360  # 确保方向在0到360度之间
                print(f"Target Direction: {self.targetDirection}")

            currentDirection = (self.direction + 360) % 360
            directionDifference = self.calculate_angle_difference(self.targetDirection, currentDirection)

            print(f"Current Direction: {currentDirection}, Difference: {directionDifference}")

            # 如果方向差距大于一定阈值（比如10度），继续转向
            if abs(directionDifference) > 30:
                self.inTurningCounts += 1  # 计数器，用于调试或其他逻辑
                return "LEFT"
            else:
                # 方向差距足够小，可以直行
                self.inTurningCounts = 0
              
                return "FORWARD"
        else:
            message = random.choice(["FORWARD","1"])
            return message
        
    
    def determine_direction(self):
        
        delta_x = self.locationCenterX - self.pre_locationCenterX
        delta_y = self.locationCenterY - self.pre_locationCenterY
        direction = (delta_x,delta_y)
        angle_radians = np.arctan2(delta_y, delta_x)

        angle_degrees = np.degrees(angle_radians)
        # print(f"angle_degrees = {angle_degrees}")
        self.direction  =  angle_degrees
        # print(f"direction = {self.direction}")


    def move_to_center(self,centerX,centerY):
    # 假设中心点坐标为 centerX, centerY
        centerX, centerY = 270, 238  # 例如值
        delta_x = centerX - self.locationCenterX
        delta_y = centerY - self.locationCenterY
        angle_radians = np.arctan2(delta_y, delta_x)
        angle_degrees = np.degrees(angle_radians)
        self.direction = angle_degrees