#!/usr/bin/env python

import random
import sys
import cv2
import numpy as np
import Image
import colorcorrect.algorithm as cca
from colorcorrect.util import from_pil, to_pil
from matplotlib import pyplot as plt

class ColorShapeDetector:

    def __init__(self, color, shape):
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
        shape_options = {'Triangle' : 3, 'Square' : 4, 'Circle' : 15}
        self.shape = (shape, shape_options[shape])
        #creating image kernels for morphological operations
        self.kernel_op = np.ones((2,2),np.uint8)
        self.kernel_cl = np.ones((5,5),np.uint8)
        self.possitive_color_images = []
        self.possitive_shape_images = []
        self.results_statistics = []

    def method(self, method, img):
        return {
            'None': img,
            'HistogramEq': self.histogram_equalization(img),
            'ClaheEq': self.clahe_equalization(img),
            'GreyWorld': self.grey_world(img),
            'Retinex': self.retinex_eq(img),
            'RetinexGreyWorld': self.retinex_gw_eq(img),
            'Stretch': self.stretch_eq(img),
            'GreyWorldStretch': self.gw_stretch_eq(img),
            'MaxWhite': self.max_white_eq(img)
        }[method]

    def save_histograms_and_processed_image(self, processed_image,
                                             image_name, path_to_save, method):
        # saving modified image
        cv2.imwrite(path_to_save + image_name, processed_image)
        # compute rgb histogram and save it
        color = ('b', 'g', 'r')
        fig = plt.figure(1)
        fig.text(0.5, 0.04, 'pixel value', ha='center')
        fig.text(0.04, 0.5, 'number of pixels', va='center', rotation='vertical')
        for i, col in enumerate(color):
            histr_processed = cv2.calcHist([processed_image],[i],None,[256],[0,256])
            plt.plot(histr_processed,color = col)
            plt.xlim([0,256])
            plt.title(method)
        plt.savefig(path_to_save + "histogram_" + image_name)
        plt.close()

    def opencv_to_pil(self,img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return Image.fromarray(img_rgb)

    def histogram_equalization(self, img):
        img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
        # split the image into three channels Y, CR, CB
        y,cr,cb = cv2.split(img_ycrcb)
        # equalize histogram on the saturation channel
        cv2.equalizeHist(y,y)
        img_eq = cv2.merge((y,cr,cb))
        img_eq_bgr = cv2.cvtColor(img_eq, cv2.COLOR_HSV2BGR)

        return img_eq_bgr

    def clahe_equalization(self, img):
        img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
        # split the image into three channels Y, CR, CB
        y,cr,cb = cv2.split(img_ycrcb)
        # create a CLAHE object
        clahe = cv2.createCLAHE(clipLimit = 5.0, tileGridSize = (12,12))
        clahe.apply(y,y)
        img_eq = cv2.merge((y,cr,cb))
        img_eq_bgr = cv2.cvtColor(img_eq, cv2.COLOR_YCR_CB2BGR)

        return img_eq_bgr

    def grey_world(self, img):
        # convert to pil format
        img_pil = self.opencv_to_pil(img)
        img_gw_pil = to_pil(cca.grey_world(from_pil(img_pil)))
        img_gw_opencv = cv2.cvtColor(np.array(img_gw_pil), cv2.COLOR_RGB2BGR)

        return img_gw_opencv

    def retinex_eq(self, img):
        # convert to pil format
        img_pil = self.opencv_to_pil(img)
        img_ret_pil = to_pil(cca.retinex(from_pil(img_pil)))
        img_ret_opencv = cv2.cvtColor(np.array(img_ret_pil), cv2.COLOR_RGB2BGR)

        return img_ret_opencv

    def retinex_gw_eq(self, img):
        # convert to pil format
        img_pil = self.opencv_to_pil(img)
        img_ret_gw_pil = to_pil(cca.retinex_with_adjust(from_pil(img_pil)))
        img_ret_gw_opencv = cv2.cvtColor(np.array(img_ret_gw_pil), cv2.COLOR_RGB2BGR)

        return img_ret_gw_opencv

    def stretch_eq(self, img):
        # convert to pil format
        img_pil = self.opencv_to_pil(img)
        img_stretch_pil = to_pil(cca.stretch(from_pil(img_pil)))
        img_stretch_opencv = cv2.cvtColor(np.array(img_stretch_pil), cv2.COLOR_RGB2BGR)

        return img_stretch_opencv

    def gw_stretch_eq(self, img):
        # convert to pil format
        img_pil = self.opencv_to_pil(img)
        img_gw_pil = to_pil(cca.grey_world(from_pil(img_pil)))
        img_gw_stretch_pil = to_pil(cca.stretch(from_pil(img_gw_pil)))
        img_gw_stretch_opencv = cv2.cvtColor(np.array(img_gw_stretch_pil), cv2.COLOR_RGB2BGR)

        return img_gw_stretch_opencv

    def max_white_eq(self, img):
        # convert to pil format
        img_pil = self.opencv_to_pil(img)
        img_max_white_pil = to_pil(cca.max_white(from_pil(img_pil)))
        img_max_white__opencv = cv2.cvtColor(np.array(img_max_white_pil), cv2.COLOR_RGB2BGR)

        return img_max_white__opencv

    def empty_list(self):
        del self.possitive_color_images[:]
        del self.possitive_shape_images[:]
        del self.results_statistics[:]

    def include_possitive_color_image(self,img):
        self.possitive_color_images.append(img)

    def include_possitive_shape_image(self,img):
        self.possitive_shape_images.append(img)

    def include_results_statistics (self, img_method):
        self.results_statistics.append(cv2.meanStdDev(img_method))

    def detect_color_shape(self, inImg_dir, method, path_to_save, get_results =
                         0 ):

        inImg = cv2.imread(inImg_dir)
        image_name = inImg_dir.strip('dataset/')
        # print image_name
        # color detection process
        inImg_filtered = cv2.GaussianBlur(inImg, (3,3),0)

        # HSV saturation value equalization
        inImg_method = self.method(method,inImg_filtered)

        if get_results == 1:
            # Calculate the statistics of the preprocessed image
            self.include_results_statistics(inImg_method)

            #saving the processed image histogram
            self.save_histograms_and_processed_image(inImg_method, image_name,
                                                     path_to_save, method)

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

            #check if the color filter succeed
            if area_ev > 75:
                self.include_possitive_color_image(inImg_dir)
                #appliying the shape filter
                if(self.shape[0] == 'Circle') :
                    circles = cv2.HoughCircles(mask_final,cv2.cv.CV_HOUGH_GRADIENT,1,5,param1=20,param2=10,minRadius=5,maxRadius=0)
                    if circles is not None:
                        self.include_possitive_shape_image(inImg_dir)
                else:
                    if len(cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)) == self.shape[1]:
                        self.include_possitive_shape_image(inImg_dir)
