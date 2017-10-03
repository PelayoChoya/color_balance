#!/usr/bin/env python

from color_detection import color_detector_handler

if __name__ == '__main__':
    colors = ['Red', 'Blue', 'Green']
    cdh = color_detector_handler.ColorDetectorHandler('dataset')
    for color in colors:
        cdh.detection_process(color)
        print color, cdh.results_per_color_number(color), cdh.images_per_color_number(color)
