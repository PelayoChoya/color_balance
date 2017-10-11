#!/usr/bin/env python

import rospy
import random
import sys
import cv2
import numpy as np

class ColorDetector:

    def __init__(self, color):
        self.number_success = 0
        #creating a filter
        #dictionary containing a color and its threshold
        #Position 0 is the lower limit and positon 1 the upper one
        color_options = {'Blue': np.array([[102,50,50],[130,255,255]]),
                         'Red': (np.array([[0, 100, 100],[20, 255,
                                                          255]]),np.array([[160,
                                                                            100,
                                                                            100],[179,
                                                                                  255,
                                                                                  255]])),
                         'Green': np.array([[49,50,50],[80, 255, 255]])}
        self.color = (color, color_options[color])
        #creating image kernels for morphological operations
        self.kernel_op = np.ones((3,3),np.uint8)
        self.kernel_cl = np.ones((9,9),np.uint8)
        self.possitive_images = []

    def method(self, method, img):
        return {
            'None': img,
            'HistogramEq': self.histogram_equalization(img),
            'ClaheEq': self.clahe_equalization(img)
        }[method]

    def histogram_equalization(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # split the image into three channels H,S,V
        h,s,v = cv2.split(img_hsv)
        # equalize histogram on the saturation channel
        cv2.equalizeHist(s, s)
        img_eq = cv2.merge((h,s,v))
        img_eq_bgr = cv2.cvtColor(img_eq, cv2.COLOR_HSV2BGR)

        return img_eq_bgr

    def clahe_equalization(self, img):
        img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
        # split the image into three channels Y, CR, CB
        y,cr,cb = cv2.split(img_ycrcb)
        # create a CLAHE object
        clahe = cv2.createCLAHE(clipLimit = 20.0, tileGridSize = (8,8))
        clahe.apply(y,y)
        img_eq = cv2.merge((y,cr,cb))
        img_eq_bgr = cv2.cvtColor(img_eq, cv2.COLOR_YCR_CB2BGR)

        return img_eq_bgr

    def empty_list(self):
        del self.possitive_images[:]

    def include_possitive_image(self,img):
        self.possitive_images.append(img)

    def detect_color(self,inImg_dir,method):

        inImg = cv2.imread(inImg_dir)

        # color detection process
        inImg_filtered = cv2.GaussianBlur(inImg, (5,5),0)

        # HSV saturation value equalization
        inImg_method = self.method(method,inImg_filtered)

        #convertion from rgb to hsv
        inImg_hsv = cv2.cvtColor(inImg_method, cv2.COLOR_BGR2HSV)


        #appliying the color filter
        if (self.color[0] == 'Red'):
            mask1 = cv2.inRange(inImg_hsv,self.color[1][0][0],
                                self.color[1][0][1])
            mask2 = cv2.inRange(inImg_hsv,self.color[1][1][0],
                                self.color[1][1][1])
            mask = cv2.bitwise_or(mask1,mask2)
        else:
            mask = cv2.inRange(inImg_hsv,self.color[1][0], self.color[1][1])

        #morphological transformation
        #kernel = np.ones((7,7),np.uint8)
        mask_op = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel_op)
        mask_op_cl = cv2.morphologyEx(mask_op, cv2.MORPH_CLOSE, self.kernel_cl)

        #removing the small objects from the binary image
        contours,h = cv2.findContours(mask_op_cl,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask_final = np.ones(mask_op_cl.shape[:2], dtype="uint8") * 255
        area_ev = 0
        iterator = 0
        biggest_area_index = 0

        if contours:
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if (area > area_ev):
                    area_ev = area
                    biggest_area_index = iterator
                    iterator = iterator + 1

            cnt =  contours[biggest_area_index]
            cv2.drawContours(mask_final, [cnt], -1, 0, -1)
            cv2.bitwise_not(mask_final,mask_final)

            #check if the color filer succeed
            if area_ev > 150:
                self.include_possitive_image(inImg_dir)
