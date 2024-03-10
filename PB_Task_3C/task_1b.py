'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1B of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_1b.py
# Functions:		detect_Qr_details, detect_ArUco_details
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import numpy as np
import cv2
from cv2 import aruco
import math
from pyzbar import pyzbar
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def detect_Qr_details(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the message encrypted in the Qr code is the key and the center
    co-ordinates of the Qr code is the value, for each item in the dictionary

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `Qr_codes_details` : { dictionary }
            dictionary containing the details regarding the Qr code
    
    Example call:
    ---
    Qr_codes_details = detect_Qr_details(image)
    """    
    Qr_codes_details = {} 
    decodedObjects = pyzbar.decode(image)
    def final(data,point):
                (top_Left, top_Right, bottom_Right, bottom_Left) = point
                TR = (int(top_Right[0]), int(top_Right[1]))
                BR = (int(bottom_Right[0]), int(bottom_Right[1]))
                BL = (int(bottom_Left[0]), int(bottom_Left[1]))
                TL = (int(top_Left[0]), int(top_Left[1]))
                centre = [int((BL[0]+TR[0])/2),int((BL[1]+TR[1])/2)]
                Qr_codes_details[data] =  centre
    for obj in decodedObjects:
        data = obj.data.decode()
        point = obj.polygon
        final(data,point)
    return Qr_codes_details    

def detect_ArUco_details(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the id of the ArUco marker is the key and a list of details of the marker
    is the value for each item in the dictionary. The list of details include the following
    parameters as the items in the given order
        [center co-ordinates, angle from the vertical, list of corner co-ordinates] 
    This order should be strictly maintained in the output

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `ArUco_details_dict` : { dictionary }
            dictionary containing the details regarding the ArUco marker
    
    Example call:
    ---
    ArUco_details_dict = detect_ArUco_details(image)
    """    
    ArUco_details_dict = {} #should be sorted in ascending order of ids
    ArUco_corners = {}
    aruco_image = image
    Aruco_Dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)
    Aruco_Params = cv2.aruco.DetectorParameters_create()
    (marker_corners, marker_id, rejected_markers) = cv2.aruco.detectMarkers(aruco_image, Aruco_Dict,parameters=Aruco_Params)
    def output1(markerID,cX,cY,R,centre):
        Aruco_a=[]
        centre = [cX,cY]
        alphaR = int(round(math.degrees(math.atan2((R[1]-cY),(R[0]-cX)))))
        alphaR = (alphaR)
        Aruco_a.append(centre)
        Aruco_a.append(alphaR)
        ArUco_details_dict.update({markerID:Aruco_a})
    def corners(markerID,y1,y2,y3,y4,z1,z2,z3,z4):
        b1 = [int(y1),int(z1)]
        b2 = [int(y2),int(z2)]
        b3 = [int(y3),int(z3)]
        b4 = [int(y4),int(z4)]
        ArUco_corner=[]
        ArUco_corner.append(b1)
        ArUco_corner.append(b2)
        ArUco_corner.append(b3)
        ArUco_corner.append(b4)
        ArUco_corners.update({markerID:ArUco_corner})
        
    if len(marker_corners) > 0:
        marker_id = marker_id.flatten()
        for (markerCorner, markerID) in zip(marker_corners, marker_id):
            marker_corners = markerCorner.reshape((4, 2))
            (top_Left, top_Right, bottom_Right, bottom_Left) = marker_corners
            top_Right = (int(top_Right[0]), int(top_Right[1]))
            bottom_Right = (int(bottom_Right[0]), int(bottom_Right[1]))
            bottom_Left = (int(bottom_Left[0]), int(bottom_Left[1]))
            top_Left = (int(top_Left[0]), int(top_Left[1]))
            cX = int((top_Right[0] + bottom_Left[0]) / 2)
            cY = int((top_Right[1] + bottom_Left[1]) / 2)
            x1 = top_Right
            x2 = top_Left
            x3 = bottom_Right
            x4 = bottom_Left
            y1 = int(top_Right[0]);z1 = int(top_Right[1])
            y2 = int(bottom_Right[0]);z2 =int(bottom_Right[1])
            y3 = int(bottom_Left[0]);z3 =int(bottom_Left[1])
            y4 = int(top_Left[0]);z4=int(top_Left[1])
            corners(int(markerID),y1,y2,y3,y4,z1,z2,z3,z4)
            U = ((x1[0]+x2[0])/2,(x1[1]+x2[1])/2)
            D = ((x3[0]+x4[0])/2,(x3[1]+x4[1])/2)
            R = ((x1[0]+x3[0])/2,(x1[1]+x3[1])/2)
            L = ((x4[0]+x2[0])/2,(x4[1]+x2[1])/2)
            centre = [cX,cY]
            output1(int(markerID),cX,cY,R,centre)
        ##################################################
        
    return ArUco_details_dict, ArUco_corners 

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE CODE BELOW #########	

# marking the Qr code with center and message

def mark_Qr_image(image, Qr_codes_details):
    for message, center in Qr_codes_details.items():
        encrypted_message = message
        x_center = int(center[0])
        y_center = int(center[1])
        
        cv2.circle(img, (x_center, y_center), 5, (0,0,255), -1)
        cv2.putText(image,str(encrypted_message),(x_center + 20, y_center+ 20),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

    return image

# marking the ArUco marker with the center, angle and corners

def mark_ArUco_image(image,ArUco_details_dict, ArUco_corners):

    for ids, details in ArUco_details_dict.items():
        center = details[0]
        cv2.circle(image, center, 5, (0,0,255), -1)
        corner = ArUco_corners[int(ids)]
        cv2.circle(image, (int(corner[0][0]), int(corner[0][1])), 5, (50, 50, 50), -1)
        cv2.circle(image, (int(corner[1][0]), int(corner[1][1])), 5, (0, 255, 0), -1)
        cv2.circle(image, (int(corner[2][0]), int(corner[2][1])), 5, (128, 0, 255), -1)
        cv2.circle(image, (int(corner[3][0]), int(corner[3][1])), 5, (255, 255, 255), -1)

        tl_tr_center_x = int((corner[0][0] + corner[1][0]) / 2)
        tl_tr_center_y = int((corner[0][1] + corner[1][1]) / 2) 

        cv2.line(image,center,(tl_tr_center_x, tl_tr_center_y),(255,0,0),5)
        display_offset = 2*int(math.sqrt((tl_tr_center_x - center[0])**2+(tl_tr_center_y - center[1])**2))
        cv2.putText(image,str(ids),(center[0]+int(display_offset/2),center[1]),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        #angle = details[1]
        #cv2.putText(image,str(angle),(center[0]-display_offset,center[1]),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return image

if __name__ == "__main__":

    # path directory of images in test_images folder
    img_dir_path = "C:\\Users\\HARI\\Downloads\\PB_Task1_Windows\\PB_Task1_Windows\\Task1B\\public_test_cases\\"

    # choose whether to test Qr or ArUco images
    choice = input('\nWhich images do you want to test ? => "q" or "a": ')

    if choice == 'q':

        marker = 'qr'

    else:

        marker = 'aruco'

    for file_num in range(0,2):
        img_file_path = img_dir_path +  marker + '_' + str(file_num) + '.png'

        # read image using opencv
        img = cv2.imread(img_file_path)

        print('\n============================================')
        print('\nFor '+ marker  +  str(file_num) + '.png')

        # testing for Qr images
        if choice == 'q':
            Qr_codes_details = detect_Qr_details(img)
            print("Detected details of Qr: " , Qr_codes_details)

            # displaying the marked image
            img = mark_Qr_image(img, Qr_codes_details)
            cv2.imshow("img",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # testing for ArUco images
        else:    
            ArUco_details_dict, ArUco_corners = detect_ArUco_details(img)
            print("Detected details of ArUco: " , ArUco_details_dict)

            #displaying the marked image
            img = mark_ArUco_image(img, ArUco_details_dict, ArUco_corners)  
            cv2.imshow("img",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
