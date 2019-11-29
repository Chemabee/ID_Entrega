import cv2
import numpy as np
from matplotlib import pyplot as plt
import MTM

class MatchTemplate:
    def __init__(self):
        pass

    def doMatch(self, img_rgb):
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        templates = [['{}'.format(i), cv2.imread('./templates/{}.png'.format(i),0)]for i in range (10)]
        
        res = MTM.matchTemplates(templates, img_gray, method=cv2.TM_CCOEFF_NORMED, N_object=4, score_threshold=0.3, maxOverlap=0.4, searchBox=None)
        print(res)
        img_rgb = MTM.drawBoxesOnRGB(img_rgb, res, boxThickness=2, boxColor=(255, 255, 00), showLabel=True, labelColor=(255, 255, 0), labelScale=0.5 )
        num = []
        for i in range(len(res)):
            num.append([res['BBox'][i][0], res['TemplateName'][i]])
        num.sort(key = self.sortFirst)
        return img_rgb, num
    
    def sortFirst(self,val):
        return val[0]