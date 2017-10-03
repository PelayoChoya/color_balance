#!/usr/bin/env python

from color_detector import ColorDetector
import glob

class ColorDetectorHandler:

    def __init__(self, path_to_dataset_dir):
        # list containing all the images in the dataset directory
        self.image_dataset = sorted(glob.glob(path_to_dataset_dir + "/*"))
        # dictionary that contains the color, the instance of the class, 
        # the number of times it has been detected and the images where
        # the detection has been successful
        self.colors = {'Red': [ColorDetector('Red'), 0,[]],
                                  'Blue':
                                  [ColorDetector('Blue'),0,[]],
                                  'Green':
                                  [ColorDetector('Green'),0,[]]}

    def success_per_color_update(self, color, number):
        self.colors[color][1] = number

    def success_per_color_number(self,color):
        return self.colors[color][1] 

    def successful_images_per_color_update(self, color, images):
        self.colors[color][2] = images 

    def successful_images_per_color_number(self,color):
        return self.colors[color][2] 

    def detection_process(self, color):
        for image in self.image_dataset:
            self.colors[color][0].detect_color(image)
        self.success_per_color_update(color, self.colors[color][0].number_success)
        self.successful_images_per_color_update(color,
                                                self.colors[color][0].possitive_images)
