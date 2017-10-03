#!/usr/bin/env python

from color_detector import ColorDetector
import glob

class ColorDetectorHandler:

    def __init__(self, path_to_dataset_dir):
        # list containing all the images in the dataset directory
        self.image_dataset = sorted(glob.glob(path_to_dataset_dir + "/*"))
        self.detectable_colors = {'Red': ColorDetector('Red'),
                                  'Blue':
                                  ColorDetector('Blue'),
                                  'Green':
                                  ColorDetector('Green')}
    def detection_process(self, color):
        for image in self.image_dataset:
            self.detectable_colors[color].detect_color(image)
        print self.detectable_colors[color].number_success
        print self.detectable_colors[color].possitive_images
