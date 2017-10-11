#!/usr/bin/env python

from color_detection import color_detector_handler

if __name__ == '__main__':
    colors = ['Red', 'Blue', 'Green']
    methods = ['None', 'HistogramEq', 'ClaheEq', 'GrayWorld']
    cdh = color_detector_handler.ColorDetectorHandler('dataset')
    for method in methods:
        print method
        for color in colors:
            cdh.detection_process(color, method)
            print "\t", color, cdh.results_per_color_number(color)#, cdh.images_per_color_number(color)
            cdh.empty_results(color)
