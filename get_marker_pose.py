# Program to get pose from 2D Markers
import sys
import getopt
import joblib
import math

import numpy as np 
import cv2

import marker_utils as mu

def parse_options(argv):
    """Parse the arguments of this program"""
    image_file = ''
    if len(argv) == 0:
        print("get_marker_pose.py -i <image>")
        sys.exit(2)
    try:
        opts, _ = getopt.getopt(argv, 'hi:', ['image='])
    except getopt.GetoptError:
        print("get_marker_pose.py -i <image>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("get_marker_pose.py -i <image>")
            sys.exit()
        elif opt in ("-i", "--image"):
            image_file = arg
    print("Image file: ", image_file)

    return image_file

def mat_to_rpy(mat):
    """Convert rotation matrix to Roll.Pitch-Yaw representation"""
    roll = math.atan2(mat[2, 1], mat[2, 2])
    pitch = math.atan2(-mat[2, 0], math.sqrt(1 - mat[2, 0]**2))
    yaw = math.atan2(mat[1, 0], mat[0, 0])

    return np.asarray([roll, pitch, yaw], dtype=np.float)

if __name__ == '__main__':
    # Read test image with the markers
    image_addr = parse_options(sys.argv[1:])
    image = cv2.imread(image_addr)
    # image = cv2.resize(image, None, fx=0.25, fy=0.25)
    # cv2.imwrite("im.png", image)

    # Detect markers
    corners, detected_markers = mu.detect_markers(image)
    # print("Corners:\n", corners)

    # First, we define the camera parameters
    cameraMatrix = np.array([[791.0, 0, 500.0], [0, 791.0, 375.0], [0, 0, 1]])
    distCoefs = np.array([[0, 0, 0, 0, 0]])
    markerLength = 35 # mm

    rotations, translations = mu.estimate_marker_pose(image, corners, cameraMatrix, distCoefs, markerLength)
    # rot, tr, objPoints = ar.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoefs)

    # Display image
    # outputImage = image.copy()
    # outputImage = ar.drawDetectedMarkers(outputImage, corners, ids)
    for i in range(len(rotations)):
        rotMat, _ = cv2.Rodrigues(rotations[i])
        rpy = mat_to_rpy(rotMat)
        print("Marker {0} pose: \nRot (Roll, Pitch, Yaw): {1}\nTranslation (X, Y , Z): {2}".format(i, np.rad2deg(rpy), translations[i]))
        detected_markers = mu.draw_axes(detected_markers, rotations[i], translations[i], cameraMatrix, distCoefs, markerLength)
    
    cv2.imshow('Detected markers', detected_markers)
    cv2.waitKey(0)
    cv2.destroyAllWindows()