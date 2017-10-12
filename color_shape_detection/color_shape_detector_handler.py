#!/usr/bin/env python

from color_shape_detector import ColorShapeDetector
import glob
import collections

class ColorShapeDetectorHandler:

    def __init__(self, path_to_dataset_dir):
        # list containing all the images in the dataset directory
        self.image_dataset = sorted(glob.glob(path_to_dataset_dir + "/*"))
        # dictionary that contains the color, the instance of the class,
        # the number of times it has been detected and the images where
        # the detection has been successful
        shapes = {}
        self.detection = collections.defaultdict(dict)
        color_options = ['Red','Blue','Green']
        shape_options = ['Circle', 'Triangle', 'Square']

        for color in color_options:
            for shape in shape_options:
                self.detection[color][shape]=({'Instance': ColorShapeDetector(color,shape)})
                self.detection[color][shape].update({'ColorSuccessNumber' : 0})
                self.detection[color][shape].update({'ColorFailNumber' : 0})
                self.detection[color][shape].update({'ColorSucessfulImages' :
                                                []})
                self.detection[color][shape].update({'ColorFailImages' : []})
                self.detection[color][shape].update({'ShapeSuccessNumber' : 0})
                self.detection[color][shape].update({'ShapeFailNumber' : 0})
                self.detection[color][shape].update({'ShapeSucessfulImages' :
                                                []})
                self.detection[color][shape].update({'ShapeFailImages' : []})

    def empty_results(self, color, shape):
        self.detection[color][shape]['Instance'].empty_list()
        self.results_per_color_update(color, shape,
                                      self.detection[color][shape]['Instance'].possitive_images)
        self.images_per_color_update(color, shape,
                                                self.detection[color][shape]['Instance'].possitive_images)

    def results_per_color_update(self, color, shape, images):
        self.detection[color][shape]['ColorSuccessNumber'] = len(filter(lambda x: color.lower() in x, images))
        self.detection[color][shape]['ColorFailNumber'] = len(images) - len(filter(lambda x: color.lower() in x, images))

    def images_per_color_update(self, color, shape, images):
        self.detection[color][shape]['ColorSuccessfulImages'] = filter(lambda x: color.lower() in x, images)
        self.detection[color][shape]['ColorFailImages'] = filter(lambda x: color.lower() not in x, images)

    def results_per_color_number(self, color, shape):
        return (self.detection[color][shape]['ColorSuccessNumber'],
                self.detection[color][shape]['ColorFailNumber'])

    def images_per_color_number(self,color, shape):
        return (self.detection[color][shape]['ColorSuccessfulImages'],
                self.detection[color][shape]['ColorFailImages'])

    def detection_process(self, color, shape, method):
        for image in self.image_dataset:
            self.detection[color][shape]['Instance'].detect_color(image, method)
        self.results_per_color_update(color, shape,
                                      self.detection[color][shape]['Instance'].possitive_images)
        self.images_per_color_update(color, shape,
                                                self.detection[color][shape]['Instance'].possitive_images)
