#!/usr/bin/env python

from color_shape_detection import color_shape_detector_handler
import os
import numpy as np

def create_directory(name):
   directory = os.path.dirname(name)
   if not os.path.exists(directory):
       os.makedirs(directory)

def write_results(file_path, shape, color, results_color, results_shape):
    with open(file_path + "results.txt" , "a") as results_file:
        results_file.write(shape + "," + color + "\n")
        results_file.write("\n"+ "results color"+ repr(results_color) + "\n")
        results_file.write("\n"+ "results shape"+ repr(results_shape) + "\n")
        results_file.write("\n")

def write_statistics(file_path, stats):
    for key in stats:
        with open(file_path + key.lower() + "_statistics.txt" , "w") as text_file:
            text_file.write("Image after algorithm (Mean(1x3),StdDev(1x3))\n")
            text_file.write("\n")
            for stat in stats[key]:
                complete = np.concatenate((np.reshape(stat[0],(1,3)),np.reshape(stat[1],(1,3))), axis = 1)
                np.savetxt(text_file, complete,'%-7.4f')

if __name__ == '__main__':
    colors = ['Red', 'Blue', 'Green']
    shapes= ['Circle', 'Triangle', 'Square']
    methods = ['None', 'HistogramEq', 'ClaheEq', 'GreyWorld',
               'Retinex', 'RetinexGreyWorld', 'Stretch', 'GreyWorldStretch',
               'MaxWhite']
    cdh = color_shape_detector_handler.ColorShapeDetectorHandler('dataset')
    #results = []
    #for method in methods:
    #    print method
    #    file_path = os.path.dirname(os.path.abspath(__file__)) + "/results/" + method+ "/"
    #    # create results parent directory
    #    create_directory(file_path)
    #    iterator = 0
    #    for shape in shapes:
    #        for color in colors:
    #            # save histograms, images and statistics results
    #            if iterator == 8:
    #                cdh.detection_process(color, shape, method, file_path, 1)
    #                write_statistics(file_path, cdh.results_statistics(color,
    #                                                                   shape))
    #            else:
    #                cdh.detection_process(color, shape, method, file_path)
    #            # write results
    #            write_results(file_path,shape,color,
    #                          cdh.results_per_color_number(color,shape),
    #                          cdh.results_per_shape_number(color,shape))
    #            iterator += 1
    #            cdh.empty_results(color,shape)
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/results/" + \
    'None'+ "/"
    create_directory(file_path)
    for method in methods:
        cdh.detection_process('Red', 'Circle', method, file_path, 1)
    #write_statistics(file_path, cdh.results_statistics('Red','Circle'))
