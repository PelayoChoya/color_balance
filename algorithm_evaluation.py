#!/usr/bin/env python

from color_shape_detection import color_shape_detector_handler

class DataHolder:

    def __init__(self, method):
        self.method = method
        self.results = []

    def results(self, color, shape, color_results, shape_results):
        self.results.append({color:color_results, shape: shape_results})

if __name__ == '__main__':
    colors = ['Red', 'Blue', 'Green']
    shapes= ['Circle', 'Triangle', 'Square']
    methods = ['None', 'HistogramEq', 'ClaheEq', 'GreyWorld',
               'Retinex', 'RetinexGreyWorld', 'Stretch', 'GreyWorldStretch',
               'MaxWhite']
    cdh = color_shape_detector_handler.ColorShapeDetectorHandler('dataset')
    results = []
    iterator = 0
    for method in methods:
        print method
        results.append(DataHolder(method))
        for shape in shapes:
            print "\t", shape
            for color in colors:
                cdh.detection_process(color, shape, method)
                results_color = cdh.results_per_color_number(color,
                                                              shape)
                results_shape = cdh.results_per_shape_number(color,
                                                              shape)
                print "\t\t", color,results_color, results_shape
                #print results[iterator]
                # results[iterator].results(color, shape, results_color,
                #                           results_shape)
                cdh.empty_results(color,shape)
        iterator += 1
