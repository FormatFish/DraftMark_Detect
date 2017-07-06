#coding=utf-8
import cv2
from skimage import filters , io
import imutils
import numpy as np
from imutils.perspective import four_point_transform

class Image_preprocess:
    def __init__(self , filename):
        self.image = imutils.resize(cv2.imread(filename) , height = 500)
        self.gray = cv2.cvtColor(self.image , cv2.COLOR_BGR2GRAY)

    def detect_contours(self):
        gradient = filters.sobel(self.gray.astype("float"))
        # io.imshow(self.gray)
        # io.show()

        blurred = cv2.blur(gradient , (9 , 9))
        blurred = blurred.astype(np.uint8)
        _ , thresh = cv2.threshold(blurred , 20 , 255 , cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT , (21 , 7))
        self.closed = cv2.morphologyEx(thresh , cv2.MORPH_CLOSE , kernel)
        self.closed = cv2.erode(self.closed, None, iterations = 4)
        self.closed = cv2.dilate(self.closed, None, iterations = 8)
        cnts = cv2.findContours(self.closed.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        return cnts

    def alig_image(self , c):
        rect = cv2.minAreaRect(c)
        angle = rect[-1]
        #before I rotate it , I find the angle should be minus, so there are no change 
        #about angle
        (h , w) = self.image.shape[:2]
        center = cv2.moments(c)
        center = (int(center['m10']/center['m00']) , int(center['m01']/center['m00']))
        # print center , angle
        M = cv2.getRotationMatrix2D(center , angle , 1.0)
        rotated = cv2.warpAffine(self.closed.copy() , M , (w , h) , flags = cv2.INTER_CUBIC , borderMode = cv2.BORDER_REPLICATE)
        rotated_image = cv2.warpAffine(self.image.copy() , M , (w , h) , flags = cv2.INTER_CUBIC , borderMode = cv2.BORDER_REPLICATE)
        return rotated , rotated_image

    def get_target_piece(self , rotated , rotated_image):
        cnts = cv2.findContours(rotated.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        c = sorted(cnts , key = cv2.contourArea , reverse=True)[0]
        rect = cv2.minAreaRect(c)
        # print rect
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        wraped = four_point_transform(rotated_image , box.reshape(-1 , 2))
        return wraped

    def piece_detect(self , wraped):
        wraped_gray = cv2.cvtColor(wraped , cv2.COLOR_BGR2GRAY)
        gradent = filters.sobel(wraped_gray.astype("float"))
        blurred = cv2.blur(gradent , (5 , 5))
        (_, thresh) = cv2.threshold(blurred.astype("uint8"), 30, 80, cv2.THRESH_BINARY)
        cnts = cv2.findContours(thresh.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        return cnts

    def get_max_cnt_and_interval_from_pieces(self , cnts):
        cnt = 0
        max_area= cv2.contourArea(cnts[0])
        target_c = None
        for c in cnts:
            tmp = cv2.contourArea(c)
            if tmp > max_area:
                cnt += 1
                target_c = c
                max_area = tmp
            # x , y , w , h = cv2.boundingRect(c)
            # tmp = cv2.rectangle(wraped.copy() , (x , y) , (x + w , y + h) ,(0 , 0 , 255) , 2)
            # io.imshow(tmp)
            # io.show()
            
        return cnt , target_c
