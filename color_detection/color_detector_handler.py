#!/usr/bin/env python

from color_detector import ColorDetector
import glob
import collections

class ColorDetectorHandler:

    def __init__(self, path_to_dataset_dir):
        # list containing all the images in the dataset directory
        self.image_dataset = sorted(glob.glob(path_to_dataset_dir + "/*"))
        # dictionary that contains the color, the instance of the class,
        # the number of times it has been detected and the images where
        # the detection has been successful
        self.colors = collections.defaultdict(dict)
        colors = ['Red','Blue','Green']
        for color in colors:
            self.colors[color]['Instance'] = ColorDetector(color)
            self.colors[color]['SuccessNumber'] = 0
            self.colors[color]['SuccessfulImages'] = []

    def success_per_color_update(self, color, number):
        self.colors[color]['SuccessNumber'] = number

    def success_per_color_number(self,color):
        return self.colors[color]['SuccessNumber']

    def successful_images_per_color_update(self, color, images):
        self.colors[color]['SuccessfulImages'] = images

    def successful_images_per_color_number(self,color):
        return self.colors[color]['SuccessfulImages']

    def detection_process(self, color):
        for image in self.image_dataset:
            self.colors[color]['Instance'].detect_color(image)
        self.success_per_color_update(color, self.colors[color]['Instance'].number_success)
        self.successful_images_per_color_update(color,
                                                self.colors[color]['Instance'].possitive_images)
