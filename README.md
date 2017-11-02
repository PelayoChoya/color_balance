# Color balancing repo

This repo provides the necessary code to test different techniques to test preprocessing algorithms for color detection purposes

## How it works

By executing the main algorithm_evaluation python script, images will be read from the dataset directory and the results will appear in a new results directory.

The results will contain:
- A txt file with the results of the detection process (number of fails and successes per method for each color and shape)
- A txt file containing the statistics for each image after the preprocessing algorithm is applied, mean and standard deviation
- The image after the preprocessing algorithm has been applied
- An histogram of the image after the preprocessing algorithm has been applied 

