#!/usr/bin/env python

from color_detection import color_detector_handler

if __name__ == '__main__':
    cdh = color_detector_handler.ColorDetectorHandler('dataset')
    cdh.detection_process('Red')
    print cdh.results_per_color_number('Red')
    print cdh.successful_images_per_color_number('Red')
