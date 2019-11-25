import cv2

def Main():
    template_img = cv2.imread("lena_eye.jpg", CV_LOAD_IMAGE_GRAYSCALE)
    if (template_img.data == null):
        return -1
    cv2.imshow("Template Image", template_img)

    src_img = imread("lena.jpg", CV_LOAD_IMAGE_GRAYSCALE)
    if (src_img.data == null):
		return -1
    cv2.cvtColor(src_img, debug_img, CV_GRAY2BGR)

    match_method = CV_TM_CCORR_NORMED
    cv2.matchTemplate(src_img, template_img, result_mat, match_method)
    cv2.normalize(result_mat, result_mat, 0, 1, NORM_MINMAX, -1, cv2.Mat())

    cv2.minMaxLoc(result_mat, minVal, maxVal, minLoc, maxLoc, Mat())
    if(match_method == CV_TM_SQDIFF or match_method == CV_TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc
    
    cv2.rectangle(
			debug_img,
			matchLoc,
			cv2.Point(matchLoc.x + template_img.cols , matchLoc.y + template_img.rows),
			CV_RGB(255,0,0),
			3)
    cv2.imshow("Match Template", debug_img)

    c = cv2.waitKey()
    
    return 0

if __name__ == "__main__":
    Main()