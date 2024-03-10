'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy
from  numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################
from task_1b import detect_ArUco_details
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
#####################################################################################

def perspective_transform(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = [] 
#################################  ADD YOUR CODE HERE  ###############################
    a,b = detect_ArUco_details(image)
    if(1 in b and 2 in b and 3 in b and 4 in b):
            g=b[2]
            h=b[1]
            i=b[4]
            j=b[3]
    try:
        c=g[2];d=h[3];e=i[1];f=j[0]
        output_pts = numpy.float32([[0,0],[511,0],[511,511],[0,511]])
        input_pts = numpy.float32([[[f[0]-25,f[1]-10]],[[e[0]+15,e[1]-30]],[[d[0]+25,d[1]+30]],[[c[0]-10,c[1]+5]]])
        M = cv2.getPerspectiveTransform(input_pts,output_pts)
        warped_image = cv2.warpPerspective(image,M,(512, 512),flags=cv2.INTER_LINEAR)
    except:
        s=1
        ######################################################################################
    return warped_image

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    try:
            a,b = detect_ArUco_details(image)
            x=a[5]
            c=x[0][0]
            d=x[0][1]
            f = map(c, 0, 511, -0.9550, 0.9550)
            g = map(d, 0, 511, -0.9550, 0.9550)
            scene_parameters.append(f)
            scene_parameters.append(-g)
            scene_parameters.append(x[1])
    except:
            s=1
######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.
    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/aruco_5')

#################################  ADD YOUR CODE HERE  ###############################
    if(scene_parameters!=[]):
            if(90>scene_parameters[2]>=0):
                    a=0
            elif(180>scene_parameters[2]>=90):
                    a=55
            elif(-90>scene_parameters[2]>=-180):
                    a=-135
            elif(0>scene_parameters[2]>=-90):
                    a=-55
            try:
                aruco_handle1 = sim.getObject('/Arena')
                sim.setObjectPosition(aruco_handle,aruco_handle1,[scene_parameters[0],scene_parameters[1],0])
                sim.setObjectOrientation(aruco_handle,aruco_handle1,[0,0,a])
            except:
                s=1
######################################################################################

    return None

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
    #################################  ADD YOUR CODE HERE  ################################
    video = cv2.VideoCapture(0)# capturing the video from overhead camera
    while(True):
        _, frame = video.read()
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
        warped_image =perspective_transform(frame)
        scene_parameters=transform_values(warped_image)
        set_values(scene_parameters) # capturing individual frames
    ######################################################################################
    
