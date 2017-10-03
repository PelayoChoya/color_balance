#!/usr/bin/env python

from color_detector import ColorDetector
import glob
if __name__ == '__main__':
    # list containing all the images in the dataset directory
    image_dataset = sorted(glob.glob("dataset/*"))
    cd = ColorDetector('Green')
    for image in image_dataset:
        cd.detect_color(image)
    print cd.number_success
    print cd.possitive_images
