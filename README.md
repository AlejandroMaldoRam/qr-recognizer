# About the programs

Two programs are included in this solution:

1. **get_marker_pose.py**: This program takes as argument the name of an image file. It calculates the pose of the markers in the iamge with respect to the camera coordinate frame. It is assumed the typical configuration of the cameras' coordinate frame, that is, the Z axis point away from the camera, the X axis aligned with the horizontal axis of the image from left to right and the Y axis aligned with the vertical axis of the image. 
2. **generate_marker.py**: This program generates the marker used on this tests. It is possible to uso other markers as long as they encode the rotation. 

In addition to these programs, a **marker_utils.py** module is included. This contains the functions that are used in the programs. 

# Usage

The programs are used as follow:
1. `python get_marker_pose.py -i set1/im1.png`
The output of this program will be a message in the console indicating the pose of the marker as well an image indicating the detected markers with their respective coordinate frames. 

2. `python generate_marker.py -s 500`
The output of this program will be a png file named im.png. This will contain the image of the marker used for this task. The argument after the -s options indicates the size in pixels. 

# About the solution

Square markers with a code in its center are used to determine its correct orientation.
The steps to estimate the 6D pose of the markers is the following:
1. Apply an adaptive threhold to extract possible candidates to be a marker.
2. Extract the candidate contours and keep only the ones that have a minimum area. They should be convex shapes.
3. After that, the contour of each candidate is apporoximated with a polygon with fewer points. This is to get the 4 four points that compose the contour of a possible marker.
4. Only the approximated contours that contains only 4 points are kept. 
5. After that, I reproject the candidate to get its frontal view and extract the binary code. This code will help us to eliminate false positives and to get the direction of the marker. 
6. One the candidates has been validated, their corners locations and the camera intrisic parameters are used to estimate the pose of the marker with respect to the cameras coordinate frame. 

# About the examples

Two sets of images have been included: 
1. Set1: Image with only one marker rotated to test the robustness to changes in orientation of the marker.
2. Set2: Images with more than one markers and more objetct in the scene. In these images, there is a marker different to the one proposed for this test. In addition to that, the images from this set were taken from more points of views as well at different distances to test the robustness against scale. 

# Additional notes

1. A yml file is provided with the environment utilized in anaconda. This was obtained by executing conda env export. 
2. The main modules that were utilized for this solution are Numpy, scipy andd OpenCV. 
3. I have include only the design of one marker. However, these programs can be extended for other square markers. We can even encode a binary code in the central part of the markers. 