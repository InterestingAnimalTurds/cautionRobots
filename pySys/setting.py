import numpy as np



canvas_height = 480*2 + 100
canvas_width = 640*2 + 100





LH = 0
LS = 0
LV = 238
UH = 88
US = 255
UV = 255
lower_HSV = np.array([LH,LS,LV],np.uint8)
upper_HSV = np.array([UH,US,UV],np.uint8)