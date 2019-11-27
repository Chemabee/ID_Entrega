import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('capturas/capturas_1.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('templates/1.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED, N_object=float("inf"), score_threshold=0.5, maxOverlap=0.25, searchBox=None)
threshold = 0.8
loc = np.where( res >= threshold)
i = 0
aux = 0
for pt in zip(*loc[::-1]):
    #if((pt[1]+w-aux) > 30):
    #aux = pt[1]+w
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    print(pt) 
    i+=1
print(i)
cv2.imwrite('res.png',img_rgb)