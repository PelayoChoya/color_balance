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
            self.colors[color]['FailNumber'] = 0
            self.colors[color]['SucessfulImages'] = []
            self.colors[color]['FailImages'] = []

    def results_per_color_update(self, color, images):
        self.colors[color]['SuccessNumber'] = len(filter(lambda x: color.lower() in x, images))
        self.colors[color]['FailNumber'] = len(images) - len(filter(lambda x: color.lower() in x, images))

    def images_per_color_update(self, color, images):
        self.colors[color]['SuccessfulImages'] = filter(lambda x: color.lower() in x, images)
        self.colors[color]['FailImages'] = filter(lambda x: color.lower() not in x, images)

    def results_per_color_number(self, color):
        return (self.colors[color]['SuccessNumber'],
                self.colors[color]['FailNumber'])

    def images_per_color_number(self,color):
        return (self.colors[color]['SuccessfulImages'],
                self.colors[color]['FailImages'])

    def detection_process(self, color):
        for image in self.image_dataset:
            self.colors[color]['Instance'].detect_color(image)
        self.results_per_color_update(color,
                                      self.colors[color]['Instance'].possitive_images)
        self.images_per_color_update(color,
                                                self.colors[color]['Instance'].possitive_images)
