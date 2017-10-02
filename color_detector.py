#!/usr/bin/env python

import rospy
import random
import sys
import cv2
import numpy as np

class ColorDetector:

    def __init__(self):
        self.success_color = False
        self.detected_color = ''

        #creating a filter
        #Position 0 is the lower limit and positon 1 the upper one
        blue_threshold = np.array([[103,50,50],[130,255,255]])
        red_threshold = np.array([[169, 100, 100],[189, 255, 255]])
        green_threshold = np.array([[49,50,50],[80, 255, 255]])
        self.colors = {'Blue': blue_threshold, 'Red': red_threshold, 'Green': green_threshold, }

        #creating image kernels for morphological operations
        self.kernel_op = np.ones((3,3),np.uint8)
        self.kernel_cl = np.ones((9,9),np.uint8)

    def detect_color(self,inImg_dir):

        inImg = cv2.imread(inImg_dir)
        dim = (1280,720)
        print(dim)
        # perform the actual resizing of the image and show it
        inImg_resized = cv2.resize(inImg, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("resized", inImg_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        for color in self.colors:
            print(color)
            inImg_filtered = cv2.GaussianBlur(inImg_resized, (5,5),0)

            #convertion from rgb to hsv
            inImg_hsv = cv2.cvtColor(inImg_filtered, cv2.COLOR_BGR2HSV)

            #appliying the color filter
            mask = cv2.inRange(inImg_filtered,self.colors[color][0], self.colors[color][1])
            cv2.imshow("mask", mask)


            #morphological transformation
            #kernel = np.ones((7,7),np.uint8)
            mask_op = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel_op)
            mask_op_cl = cv2.morphologyEx(mask_op, cv2.MORPH_CLOSE, self.kernel_cl)
            #cv2.imshow("mask opening closing", mask_op_cl)


            #removing the small objects from the binary image
            contours,h = cv2.findContours(mask_op_cl,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            mask_final = np.ones(mask_op_cl.shape[:2], dtype="uint8") * 255
            #cv2.imshow("middle step", mask_final)
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
                cv2.imshow("hue", mask_final)
                #check if the color filer succeed
                if area_ev > 20000:
                    self.detected_color = color
                    self.success_color = True
                elif area_ev < 20000 and not self.success_color:
                    self.detected_color = 'None'

                cv2.waitKey(0)
                self.success_color = False
