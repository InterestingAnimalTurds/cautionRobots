import numpy as np
def calculate_angle_difference(target_angle, current_angle):
    diff = (target_angle - current_angle + 360) % 360
    if diff > 180:
        diff -= 360
    return diff

def normalize_angle(angle):
    if angle > 180:
        angle -= 360
    elif angle <= -180:
        angle += 360
    return angle

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)




















# def keyLogic(key):
#     global robots

#     if key == ord('r'):  # 如果按下's'键，则打印信息
#             message = 'LED1'
#             print(f"Sending: {message}")
#             sent = sock.sendto(message.encode(), esp32_addr)
#     elif key == ord('e'):  # 如果按下's'键，则打印信息
#             message = 'LED0'
#             print(f"Sending: {message}")
#             sent = sock.sendto(message.encode(), esp32_addr)
#     elif key == ord('s'):  # 如果按下's'键，则打印信息
#             #message = 'FORWARD'
#             for robot in robots:
#                 robot.walk(sock)
#             #print(f"Sending: {message}")
#             #sent = sock.sendto(message.encode(), esp32_addr)
#     elif key == ord('w'):  # 如果按下's'键，则打印信息
#             message = 'FORWARD'
#             print(f"Sending: {message}")
#             sent = sock.sendto(message.encode(), esp32_addr)
#     elif key == ord('a'):  # 如果按下's'键，则打印信息
#             message = 'LEFT'
#             print(f"Sending: {message}")
#             sent = sock.sendto(message.encode(), esp32_addr)
#     elif key == ord('d'):  # 如果按下's'键，则打印信息
#             message = 'RIGHT'
#             print(f"Sending: {message}")
#             sent = sock.sendto(message.encode(), esp32_addr)
#     elif key == ord('o'):  # 如果按下's'键，则打印信息
#             message = '1'
#             print(f"Sending: {message}")
#             sent = sock.sendto(message.encode(), esp32_addr)





