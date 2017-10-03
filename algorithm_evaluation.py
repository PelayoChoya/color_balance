#!/usr/bin/env python

from color_detector_handler import ColorDetectorHandler

if __name__ == '__main__':
    cdh = ColorDetectorHandler('dataset')
    cdh.detection_process('Red')
