# program to generate a marker in a PNG file.
import sys
import getopt
import joblib
import math

import numpy as np 
import cv2

def parse_options(argv):
    """Parse the arguments of this program"""
    size = 100
    if len(argv) == 0:
        print("generate_marker.py -s <size>")
        sys.exit(2)
    try:
        opts, _ = getopt.getopt(argv, 'hs:', ['size='])
    except getopt.GetoptError:
        print("generate_marker.py -s <size>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("generate_marker.py -s <size>")
            sys.exit()
        elif opt in ("-s", "--size"):
            size = int(arg)
    print("Size length for marker in pixels: ", size)

    return size

if __name__ == "__main__":
    # create image
    size = parse_options(sys.argv[1:])
    marker = np.array([[0, 1, 1], [1, 1, 0], [1, 0, 1]]) * 255
    image = np.zeros((5, 5), dtype=np.uint8)
    image[1:4, 1:4] = marker
    image = cv2.resize(image, (size, size), interpolation=cv2.INTER_NEAREST)
    
    # Save image
    cv2.imwrite("marker.png", image)

    # Display image
    cv2.imshow("marker", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()