import cv2

class Match_Template:

    def __init__(self):
        self.template_img = None
        self.src_img = None
        self.result_mat = None
        self.minVal = None
        self.maxVal = None
        self.minLoc = None
        self.maxLoc = None

    def readTemplateImage(self):
        self.template_img = cv2.imread("lena_eye.jpg", cv2.IMREAD_GRAYSCALE)
        if (self.template_img.data == None):
            return -1
        cv2.imshow("Template Image", self.template_img)

    def readSrcImage(self):
        self.src_img = cv2.imread("lena.jpg", cv2.IMREAD_GRAYSCALE)
        if (self.src_img.data == None):
            return -1

    def matchTemplate(self):
        self.readTemplateImage()
        self.readSrcImage()
        match_method = cv2.TM_CCORR_NORMED
        #match_method = cv2.TM_SQDIFF
        self.result_mat = cv2.matchTemplate(self.src_img, self.template_img, match_method)
        cv2.normalize(self.result_mat, self.result_mat, 0, 1, cv2.NORM_MINMAX, -1)

        self.minVal, self.maxVal, self.minLoc, self.maxLoc = cv2.minMaxLoc(self.result_mat, None)
        if(match_method == cv2.TM_SQDIFF or match_method == cv2.TM_SQDIFF_NORMED):
            matchLoc = self.minLoc
        else:
            matchLoc = self.maxLoc
        
        cv2.rectangle(
                self.src_img,
                matchLoc,
                (matchLoc[0] + self.template_img.shape[1] , matchLoc[1] + self.template_img.shape[0]),
                (255,0,0),
                3)
        cv2.imshow("Match Template", self.src_img)

        c = cv2.waitKey()

if __name__ == "__main__":
    m = Match_Template()
    m.matchTemplate()