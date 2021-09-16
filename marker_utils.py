"""Functions for detecting a defined marker"""

import numpy as np
from scipy.spatial import distance
import cv2


marker_orientation_dict = {266:0, 98:3, 161:2, 140:1}
pts_dst = np.array([[0, 0], [200, 0], [200, 200], [0, 200]])

def rotate_order(corners):
    """Function to rotate points of a lists of corners"""
    return np.array([corners[3,:], corners[0, :], corners[1, :], corners[2, :]])

def get_marker_id(image, corners):
    """Function to extract the binary code in the marker"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, _ = cv2.findHomography(corners, pts_dst)
    marker = cv2.warpPerspective(gray, h, (200, 200))
    pos = [60, 100, 140]
    # filter_size = 7
    # subs_mean = 10
    # th1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, filter_size, subs_mean)
    _, th = cv2.threshold(marker, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    l = []
    for i in pos:
        for j in pos:
            b = '0'
            if th[i, j] == 255:
                b = '1'
            l.append(b)
    return int(''.join(l), 2)


def order_points(pts):
    """Function to order a set of points from the top-left in clockwise order"""
    # Sort the point with respect to their x coordinate to get the points that are most to the left and right
    x_sorted = pts[np.argsort(pts[:, 0]), :]
    pts_left = x_sorted[:2, :]
    pts_right = x_sorted[2:, :]

    # Sort the most left point with respect to the y coordinate
    pts_left = pts_left[np.argsort(pts_left[:, 1]), :]
    top_left = pts_left[0]
    bottom_left = pts_left[1]

    # Sort the most right point with respect to the y coordinate
    pts_right = pts_right[np.argsort(pts_right[:, 1]), :]
    top_right = pts_right[0]
    bottom_right = pts_right[1]

    return np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.int)

def validate_candidate(image, corners):
    """Function to determine if the detected marker candidate is a valid marker"""
    marker_id = get_marker_id(image, corners)

    if marker_id in marker_orientation_dict:
        rots = marker_orientation_dict[marker_id]
        print(rots)
        for _ in range(rots):
            corners = rotate_order(corners)
        marker_id = get_marker_id(image, corners)
        return True, corners
    else:
        return False, corners

def detect_markers(image):
    """Function to detect the four corners of a marker"""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    filter_size = 39
    subs_mean = 10
    th1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, filter_size, subs_mean)
    th1 = 255 - th1
    contours, _ = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_contours = image.copy()
   
    # Remove small contours
    min_area = 1000
    min_error_poly = 5
    cts = []
    for c in contours:
        ret = cv2.contourArea(c)
        if ret > min_area:
            approxCts = cv2.approxPolyDP(c, min_error_poly, True)
            if cv2.isContourConvex(approxCts) and len(approxCts) == 4:
                pt = np.reshape(approxCts, (4, 2))
                pt = order_points(pt)
                cts.append(pt)

    detected_contours = cv2.drawContours(detected_contours, cts, -1, (0,255,0), 3)

    # Validate candidate
    valid_corners = []
    for c in cts:
        valid, corners = validate_candidate(image, c)
        if valid:
            valid_corners.append(corners)
    
    detected_contours = cv2.drawContours(image, valid_corners, -1, (0,255,0), 3)
    
    return valid_corners, detected_contours

def estimate_marker_pose(image, corners, K, dist_coeffs, marker_length):
    """Function to estiamte marker pose"""
    rotations = []
    translations = []
    for c in corners:
        obj_pts = np.array([[-marker_length/2, marker_length/2, 0], [marker_length/2, marker_length/2, 0], [marker_length/2, -marker_length/2, 0], [-marker_length/2, -marker_length/2, 0]], dtype=np.float)
        # Estimate pose
        _, rot, tr = cv2.solvePnP(obj_pts, c.astype(np.float), K, dist_coeffs, flags=cv2.SOLVEPNP_IPPE_SQUARE)
        rotations.append(rot)
        translations.append(tr)
    return rotations, translations

def draw_axes(image, rot, tr, K, dist_coeffs, marker_length, id=0):
    """Function to draw the axes for a marker pose"""
    axes_3d = np.array([[0, 0, 0], [marker_length, 0, 0], [0, marker_length, 0], [0, 0, marker_length]], dtype=np.float)
    # print(rot.dtype)
    # print(tr.dtype)
    axes_2d, _ = cv2.projectPoints(axes_3d, rot, tr, K, dist_coeffs.astype(np.float))
    axes_2d = np.reshape(axes_2d, (4, 2)).astype(np.int)
    start_pt = (axes_2d[0, 0], axes_2d[0, 1])
    x_pt = (axes_2d[1, 0], axes_2d[1, 1])
    y_pt = (axes_2d[2, 0], axes_2d[2, 1])
    z_pt = (axes_2d[3, 0], axes_2d[3, 1])
    image = cv2.arrowedLine(image, start_pt, x_pt, (0, 0, 255), 3)
    image = cv2.arrowedLine(image, start_pt, y_pt, (0, 255, 0), 3)
    image = cv2.arrowedLine(image, start_pt, z_pt, (255, 0, 0), 3)

    cv2.putText(image, "X", x_pt, cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255))
    cv2.putText(image, "Y", y_pt, cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0))
    cv2.putText(image, "Z", z_pt, cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 0, 0))
    cv2.putText(image, "{0}".format(id), start_pt, cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 0))

    return image
