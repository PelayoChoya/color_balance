#!/usr/bin/env python

from color_shape_detection import color_shape_detector_handler

if __name__ == '__main__':
    colors = ['Red', 'Blue', 'Green']
    shapes= ['Circle', 'Triangle', 'Square']
    methods = ['None', 'HistogramEq', 'ClaheEq', 'GreyWorld',
               'Retinex', 'RetinexGreyWorld', 'Stretch', 'GreyWorldStretch',
               'MaxWhite']
    cdh = color_shape_detector_handler.ColorShapeDetectorHandler('dataset')

    for method in methods:
        print method
        for shape in shapes:
            print "\t", shape
            for color in colors:
                cdh.detection_process(color, shape, method)
                print "\t\t", color, cdh.results_per_color_number(color, shape)#, cdh.images_per_color_number(color)
                cdh.empty_results(color,shape)
