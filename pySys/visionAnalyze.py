import  cv2
import setting as st

def image_denoise(img):

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    infrared=cv2.inRange(hsv,st.lower_HSV,st.upper_HSV)
    #Morphological transformation, Dilation  	
    kernal = st.np.ones((5 ,5), "uint8")
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
                distance = st.np.sqrt((pre_center[0] - post_center[0]) ** 2 + (pre_center[1] - post_center[1]) ** 2)
                if distance < threshold:
                    found = True
                    break  
                if not found:
                    miss_centers.append(pre_center)
    return miss_centers

