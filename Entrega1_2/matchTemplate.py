import cv2
import numpy as np
from matplotlib import pyplot as plt

class MatchTemplate:
    def __init__(self, img_rgb):
        #img_rgb = cv2.imread('capturas/capturas_5.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        templates = [cv2.imread('./templates/{}.png'.format(i),0)for i in range (10)]
        
        for i in range(len(templates)):
            w, h = templates[i].shape[::-1]
            res = cv2.matchTemplate(img_gray,templates[i],cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where( res >= threshold)
            i = 0
            aux = 0
            for pt in zip(*loc[::-1]):
                if((pt[1]+w-aux) > 30):
                    aux = pt[1]+w
                    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                    i+=1
            cv2.imwrite('res.png',img_rgb)