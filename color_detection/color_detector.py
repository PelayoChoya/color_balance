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
                         'Red': np.array([[169, 100, 100],[189, 255, 255]]),
                         'Green': np.array([[49,50,50],[80, 255, 255]])}
        self.color = (color, color_options[color])
        #creating image kernels for morphological operations
        self.kernel_op = np.ones((3,3),np.uint8)
        self.kernel_cl = np.ones((9,9),np.uint8)
        self.possitive_images = []

    def increase_success_number(self):
        self.number_success += 1

    def include_possitive_image(self,img):
        self.possitive_images.append(img)

    def detect_color(self,inImg_dir):

        inImg = cv2.imread(inImg_dir)

        # color detection process
        inImg_filtered = cv2.GaussianBlur(inImg, (5,5),0)

        #convertion from rgb to hsv
        inImg_hsv = cv2.cvtColor(inImg_filtered, cv2.COLOR_BGR2HSV)

        #appliying the color filter
        mask = cv2.inRange(inImg_filtered,self.color[1][0], self.color[1][1])

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
            if area_ev > 20000:
                self.increase_success_number()
                self.include_possitive_image(inImg_dir)
