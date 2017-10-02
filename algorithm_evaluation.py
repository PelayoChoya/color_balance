#!/usr/bin/env python

from color_detector import ColorDetector

if __name__ == '__main__':
    cd = ColorDetector()
    cd.detect_color("dataset/red_001.jpg")
