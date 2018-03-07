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
        self.detection = collections.defaultdict(dict)
        shapes = {}
        color_options = ['Red','Blue','Green']
        shape_options = ['Circle', 'Triangle', 'Square']

        for color in color_options:
            for shape in shape_options:
                self.detection[color][shape]=({'Instance': ColorShapeDetector(color,shape)})
                self.detection[color][shape].update({'ColorFScore' : 0})
                self.detection[color][shape].update({'ColorSucessfulImages' :
                                                []})
                self.detection[color][shape].update({'ColorFailImages' : []})
                self.detection[color][shape].update({'ShapeFScore' : 0})
                self.detection[color][shape].update({'ShapeSucessfulImages' :
                                                []})
                self.detection[color][shape].update({'ShapeFailImages' : []})

        self.statistics = []

    def empty_results(self, color, shape):
        self.detection[color][shape]['Instance'].empty_list()
        self.update_results(color, shape,
                                      self.detection[color][shape]['Instance'].possitive_color_images,
                                        self.detection[color][shape]['Instance'].possitive_shape_images,
                                      self.detection[color][shape]['Instance'].negative_color_images,
                                        self.detection[color][shape]['Instance'].negative_shape_images)
        self.update_image_list_results(color, shape,
                                                self.detection[color][shape]['Instance'].possitive_color_images,
                                                    self.detection[color][shape]['Instance'].possitive_shape_images)
        self.update_statistics_results(color, shape,
                                       self.detection[color][shape]['Instance'].results_statistics)

    def update_results(self, color, shape, images_color, images_shape,
                       f_images_color, f_images_shape):
        Color_TP = len(filter(lambda x: color.lower() in x,images_color))
        Color_FP = len(images_color) - len(filter(lambda x: color.lower() in x, images_color))
        Color_FN = len(filter(lambda x: color.lower() in x,f_images_color))
        try:
            self.detection[color][shape]['ColorFScore'] = (2.0*float(Color_TP))/(float(2*Color_TP + Color_FN + Color_FP))
        except:
            pass

        Shape_TP = len(filter(lambda x:color.lower()+ '_' +shape.lower()in x,images_shape))
        Shape_FP = len(images_shape) -len(filter(lambda x: color.lower() + '_' + shape.lower() in x, images_shape))
        Shape_FN = len(filter(lambda x: color.lower() + '_' +shape.lower()in
                              x,f_images_shape))
        try:
            self.detection[color][shape]['ShapeFScore'] =(2.0*float(Shape_TP))/(float(2*Shape_TP + Shape_FN + Shape_FP))
        except:
            pass
    def update_image_list_results(self, color, shape, images_color,
                                  images_shape):
        self.detection[color][shape]['ColorSuccessfulImages'] = filter(lambda
                                                                       x:
                                                                       color.lower()
                                                                       in x,
                                                                       images_color)
        self.detection[color][shape]['ColorFailImages'] = filter(lambda x:
                                                                 color.lower()
                                                                 not in x,
                                                                 images_color)
        self.detection[color][shape]['ShapeSuccessfulImages'] = filter(lambda
                                                                       x:
                                                                       color.lower()
                                                                       + '_' +
                                                                        shape.lower()
                                                                       in x,
                                                                       images_shape)
        self.detection[color][shape]['ShapeFailImages'] = filter(lambda x:
                                                                 color.lower()
                                                                 + '_' +
                                                                 shape.lower()
                                                                 not in x,
                                                                 images_shape)
    def update_statistics_results(self,color, shape, stats):
        self.statistics = stats

    def results_per_color_number(self, color, shape):
        return self.detection[color][shape]['ColorFScore']

    def images_per_color(self,color, shape):
        return (self.detection[color][shape]['ColorSuccessfulImages'],
                self.detection[color][shape]['ColorFailImages'])

    def results_per_shape_number(self, color, shape):
        return self.detection[color][shape]['ShapeFScore']

    def images_per_shape(self,color, shape):
        return (self.detection[color][shape]['ShapeSuccessfulImages'],
                self.detection[color][shape]['ShapeFailImages'])

    def results_statistics(self, color, shape):
        return self.statistics

    def detection_process(self, color, shape, method, path_to_save, get_results
                        =0):
        for image in self.image_dataset:
            self.detection[color][shape]['Instance'].detect_color_shape(image,
                                                                        method,path_to_save,
                                                                       get_results)
        self.update_results(color, shape,
                                      self.detection[color][shape]['Instance'].possitive_color_images,
                                        self.detection[color][shape]['Instance'].possitive_shape_images,
                                      self.detection[color][shape]['Instance'].negative_color_images,
                                        self.detection[color][shape]['Instance'].negative_shape_images)
        self.update_image_list_results(color, shape,
                                                self.detection[color][shape]['Instance'].possitive_color_images,
                                                self.detection[color][shape]['Instance'].possitive_shape_images)
        self.update_statistics_results(color, shape,
                                       self.detection[color][shape]['Instance'].results_statistics)
