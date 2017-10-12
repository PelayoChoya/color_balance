#!/usr/bin/env python

from color_detector import ColorDetector
import collections

shapes ={}
detection = collections.defaultdict(dict)
color_options = ['Red','Blue','Green']
shape_options = ['Circle', 'Triangle', 'Square']
for color in color_options:
    for shape in shape_options:
        detection[color][shape]=({'Instance': ColorDetector(color,shape)})

for color in color_options:
    for shape in shape_options:
        detection[color][shape]['Instance'].print_color()
