import socket
import time
import sys
import cv2
import numpy as np
# 创建一个窗口
cv2.namedWindow('window')

esp32_ip = "192.168.8.215"
esp32_port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
esp32_addr = (esp32_ip,esp32_port)
#sock.connect(esp32_addr)
# msg = b"Hello ESP32"
# print("Hello")

# print("sending msg\n")
# sent = sock.sendto(msg,esp32_addr)
# print("waiting msg\n")
# # data,server = sock.recvfrom(6666)
# # print(f"Received : {data}")


while True:
    # 显示一个空白图像
    img = np.zeros((200, 500, 3), np.uint8)
    img.fill(255)
    cv2.imshow('window', img)
    
    # 等待键盘输入，参数是等待时间（毫秒）。0表示无限等待
    key = cv2.waitKey(0) & 0xFF  # 使用 & 0xFF 以确保兼容性
    
    if key == ord('q'):  # 如果按下'q'键，则退出循环
        print("Quitting...")
        break
    elif key == ord('r'):  # 如果按下's'键，则打印信息
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


cv2.destroyAllWindows()
print("Closing socket")
sock.close()


# try:
#     # 发送消息

    
#     # # 接收回复
#     # print("Waiting for reply")
#     # data, server = sock.recvfrom(4096)
#     # print(f"Received: {data.decode()}")

# finally:



