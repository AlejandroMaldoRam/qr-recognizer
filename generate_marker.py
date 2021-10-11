# program to generate a marker in a PNG file.
import sys
import getopt
#import joblib
import math

import numpy as np 
import cv2

def parse_options(argv):
    """Parse the arguments of this program"""
    size = 100
    code= '000000000'
    if len(argv) == 0:
        print("generate_marker.py -s <size> -c <binary_code>")
        sys.exit(2)
    try:
        opts, _ = getopt.getopt(argv, 'hsc:', ['size=', 'code='])
    except getopt.GetoptError:
        print("generate_marker.py -s <size> -c <binary_code>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("generate_marker.py -s <size> -c <binary_code>")
            sys.exit()
        elif opt in ("-s", "--size"):
            size = int(arg)
        elif opt in ("-c", "--code"):
            code = arg
    print("Size length for marker in pixels: ", size)

    return size, code


def code_to_vector(str_code):
    """Convert a binary string code into a 2D numpy array for fitting a QR code"""
    side = int(math.ceil(math.sqrt(len(str_code))))
    mtr = np.zeros((side+2,side+2), dtype=np.uint8)
    k = 0
    #print(mtr.shape)
    for i in range(1,side+1):
        for j in range(1,side+1):
            if k < len(str_code):
                mtr[i][j] = str_code[k]
            k += 1
            #print(mtr)
    #print(mtr)
    return mtr
        
if __name__ == "__main__":
    # create image
    size, code = parse_options(sys.argv[1:])
    marker = code_to_vector(code) * 255
    image = cv2.resize(marker, (size, size), interpolation=cv2.INTER_NEAREST)
    
    # Save image
    cv2.imwrite("marker.png", image)

    # Display image
    cv2.imshow("marker", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()