#!/usr/bin/env python

from color_shape_detection import color_shape_detector_handler
import os
import numpy as np

def create_directory(name):
   directory = os.path.dirname(name)
   if not os.path.exists(directory):
       os.makedirs(directory)

if __name__ == '__main__':
    colors = ['Red', 'Blue', 'Green']
    shapes= ['Circle', 'Triangle', 'Square']
    methods = ['None', 'HistogramEq', 'ClaheEq', 'GreyWorld',
               'Retinex', 'RetinexGreyWorld', 'Stretch', 'GreyWorldStretch',
               'MaxWhite']
    cdh = color_shape_detector_handler.ColorShapeDetectorHandler('dataset')
    results = []
    for method in methods:
        print method
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/results/" + method+ "/"

        # create results parent directory
        create_directory(file_path)
        text_file = open(file_path + "results.txt" , "w")
        text_file.write("\nOriginal Image(Mean(1x3),StdDev(1x3)), Preprocessed Image(Mean(1x3),StdDev(1x3))\n")
        for shape in shapes:
        #     print "\t", shape
            for color in colors:
                text_file.write("\n" + shape + "," + color + "\n")
                cdh.detection_process(color, shape, method, file_path)
        #         results_color = cdh.results_per_color_number(color,
        #                                                       shape)
        #         results_shape = cdh.results_per_shape_number(color,
        #                                                       shape)
        #         print "\t\t", color,results_color, results_shape
                stats = cdh.results_statistics(color, shape)
                for stat in stats:
                    complete = np.concatenate((np.reshape(stat[0],(1,6)),np.reshape(stat[1],(1,6))), axis = 1)
                    np.savetxt(text_file, complete,'%-7.4f')
                    #np.savetxt(text_file, stat[1],fmt = '%-7.2f')
        #         # print results[iterator]
        #         #  results[iterator].results(color, shape, results_color,
        #         #                           results_shape)
                cdh.empty_results(color,shape)
        text_file.close()
