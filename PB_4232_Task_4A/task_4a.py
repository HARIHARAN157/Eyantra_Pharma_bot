'''/****************
****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*
*  This script is intended for implementation of Task 4A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_4a.py
*  Created:
*  Last Modified:		02/01/2023
*  Author:				e-Yantra Team
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ PB_4232 ]
# Author List:		[ HARIHARAN S,PARTHIBAN V,AJAY PRANAV P R,MAVEENKUMAR S ]
# Filename:			task_4a.py
# Functions:		[ Comma separated list of functions in this file ]
# 					
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

##############################################################

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory,"package_models")
    arena = sim.getObject('/Arena')    
####################### ADD YOUR CODE HERE ########################
    Green_cone=sim.loadModel(packages_models_directory+"\\Green_cone.ttm")
    Green_cube=sim.loadModel(packages_models_directory+"\\Green_cube.ttm")
    Green_cylinder=sim.loadModel(packages_models_directory+"\\Green_cylinder.ttm")
    Orange_cone=sim.loadModel(packages_models_directory+"\\Orange_cone.ttm")
    Orange_cube=sim.loadModel(packages_models_directory+"\\Orange_cube.ttm")
    Orange_cylinder=sim.loadModel(packages_models_directory+"\\Orange_cylinder.ttm")
    Pink_cone=sim.loadModel(packages_models_directory+"\\Pink_cone.ttm")
    Pink_cube=sim.loadModel(packages_models_directory+"\\Pink_cube.ttm")
    Pink_cylinder=sim.loadModel(packages_models_directory+"\\Pink_cylinder.ttm")
    Skyblue_cone=sim.loadModel(packages_models_directory+"\\SkyBlue_cone.ttm")
    Skyblue_cube=sim.loadModel(packages_models_directory+"\\Skyblue_cube.ttm")
    Skyblue_cylinder=sim.loadModel(packages_models_directory+"\\Skyblue_cylinder.ttm")
    model=[Green_cone,Green_cube,Green_cylinder,Orange_cone,Orange_cube,Orange_cylinder,Pink_cone,Pink_cylinder,Pink_cube,Skyblue_cone,Skyblue_cube,Skyblue_cylinder]
    model_name = ["Green_cone","Green_cube","Green_cylinder","Orange_cone","Orange_cube","Orange_cylinder","Pink_cone","Pink_cylinder","Pink_cube","Skyblue_cone","Skyblue_cube","Skyblue_cylinder"]
    for i in range(len(model)):
        model_int=sim.setObjectAlias(model[i],model_name[i])
    n=0;m=0;o=0;g=0;f=0
    for i in range(len(medicine_package_details)):
        if(medicine_package_details[i][0]):
            a=medicine_package_details[i][1]
            b=medicine_package_details[i][2]
            shop=medicine_package_details[i][0]
            if(b=='Circle'):
                b='cylinder'
            elif(b=='Triangle'):
                b='cone'
            elif(b=='Square'):
                b='cube'
            c=a+"_"+b
            if(c=='Green_cone'):
                d=Green_cone
            elif(c=='Green_cube'):
                d=Green_cube
            elif(c=='Green_cylinder'):
                d=Green_cylinder
            elif(c=='Orange_cone'):
                d=Orange_cone
            elif(c=='Orange_cube'):
                d=Orange_cube
            elif(c=='Orange_cylinder'):
                d=Orange_cylinder
            elif(c=='Pink_cone'):
                d=Pink_cone
            elif(c=='Pink_cube'):
                d=Pink_cube
            elif(c=='Pink_cylinder'):
                d=Pink_cylinder
            elif(c=='Skyblue_cone'):
                d=Skyblue_cone
            elif(c=='Skyblue_cube'):
                d=Skyblue_cube
            elif(c=='Skyblue_cylinder'):
                d=Skyblue_cylinder
        if(shop=='Shop_1'):
            if(m==0):
                sim.setObjectPosition(d,arena,[-0.83,0.675,0.0150])
                m=m+1
            elif(m==1):
                sim.setObjectPosition(d,arena,[-0.75,0.675,0.0150])
                m=m+1
            elif(m==2):
                sim.setObjectPosition(d,arena,[-0.67,0.675,0.0150])
                m=m+1
            elif(m==3):
                sim.setObjectPosition(d,arena,[-0.59,0.675,0.0150])
        elif(shop=='Shop_2'):
            if(n==0):
                sim.setObjectPosition(d,arena,[-0.44,0.675,0.0150])
                n=n+1
            elif(n==1):
                sim.setObjectPosition(d,arena,[-0.36,0.675,0.0150])
                n=n+1
            elif(n==2):
                sim.setObjectPosition(d,arena,[-0.30,0.675,0.0150])
                n=n+1
            elif(n==3):
                sim.setObjectPosition(d,arena,[-0.22,0.675,0.0150])
        elif(shop=='Shop_3'):
            if(o==0):
                sim.setObjectPosition(d,arena,[-0.12,0.675,0.0150])
                o=o+1
            elif(o==1):
                sim.setObjectPosition(d,arena,[-0.04,0.675,0.0150])
                o=o+1
            elif(o==2):
                sim.setObjectPosition(d,arena,[0.04,0.675,0.0150])
                o=o+1
            elif(o==3):
                sim.setObjectPosition(d,arena,[0.12,0.675,0.0150])
        elif(shop=='Shop_4'):
            if(f==0):
                sim.setObjectPosition(d,arena,[0.26,0.675,0.0150])
                f=f+1
            elif(f==1):
                sim.setObjectPosition(d,arena,[0.34,0.675,0.0150])
                f=f+1
            elif(f==2):
                sim.setObjectPosition(d,arena,[0.42,0.675,0.0150])
                f=f+1
            elif(f==3):
                sim.setObjectPosition(d,arena,[0.40,0.675,0.0150])
        elif(shop=='Shop_5'):
            if(g==0):
                sim.setObjectPosition(d,arena,[0.61,0.675,0.0150])
                g=g+1
            elif(g==1):
                sim.setObjectPosition(d,arena,[0.69,0.675,0.0150])
                g=g+1
            elif(g==2):
                sim.setObjectPosition(d,arena,[0.77,0.675,0.0150])
                g=g+1
            elif(g==3):
                sim.setObjectPosition(d,arena,[0.85,0.675,0.0150])
        all_models.append(d)
    remove=[]
    for i in range(len(model)):
        if model[i] not in all_models:
            remove.append(model[i])
    for k in range(len(remove)):
        sim.removeModel(remove[k])
####################################################################
    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')
    ####################### ADD YOUR CODE HERE ######################### 
    trafic=[]
    for k in range(len(traffic_signals)):
        traffic=sim.loadModel(traffic_sig_model)
        trafic.append(traffic)
    nodes  =   [['A1','B1','C1','D1','E1','F1'],
				['A2','B2','C2','D2','E2','F2'],
				['A3','B3','C3','D3','E3','F3'],
				['A4','B4','C4','D4','E4','F4'],
				['A5','B5','C5','D5','E5','F5'],
				['A6','B6','C6','D6','E6','F6']]
    ordinates =[[[-0.89,0.89,0.15588],[-0.53,0.89,0.15588],[-0.17,0.89,0.15588],[0.19,0.89,0.15588],[0.55,0.89,0.15588],[0.89,0.89,0.15588]],
                [[-0.89,0.53,0.15588],[-0.53,0.53,0.15588],[-0.17,0.53,0.15588],[0.19,0.53,0.15588],[0.55,0.53,0.15588],[0.89,0.53,0.15588]],
                [[-0.89,0.17,0.15588],[-0.53,0.17,0.15588],[-0.17,0.17,0.15588],[0.19,0.17,0.15588],[0.55,0.17,0.15588],[0.89,0.17,0.15588]],
                [[-0.89,-0.18,0.15588],[-0.53,-0.18,0.15588],[-0.17,-0.18,0.15588],[0.19,-0.18,0.15588],[0.55,-0.18,0.15588],[0.89,-0.18,0.15588]],
                [[-0.89,-0.53,0.15588],[-0.53,-0.53,0.15588],[-0.17,-0.53,0.15588],[0.19,-0.53,0.15588],[0.55,-0.53,0.15588],[0.89,-0.53,0.15588]],
                [[-0.89,-0.88,0.15588],[-0.53,-0.88,0.15588],[-0.17,-0.88,0.15588],[0.19,-0.88,0.15588],[0.55,-0.88,0.15588],[0.89,-0.88,0.15588]]]
    co=[]
    for i in range(len(traffic_signals)):
        for w in range(0,6):
            for x in range(0,6):
                if(nodes[w][x]==traffic_signals[i]):
                    co.append(ordinates[w][x])
    for k in range(len(co)):
        sim.setObjectPosition(trafic[k],arena,co[k])
    all_models.extend(trafic)
    for i in range(len(trafic)):
        model_int=sim.setObjectAlias(trafic[i],"Signal_"+traffic_signals[i])
####################################################################
    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')  
####################### ADD YOUR CODE HERE #########################
    start=sim.loadModel(start_node_model)
    end =sim.loadModel(end_node_model)
    nodes  =   [['A1','B1','C1','D1','E1','F1'],
				['A2','B2','C2','D2','E2','F2'],
				['A3','B3','C3','D3','E3','F3'],
				['A4','B4','C4','D4','E4','F4'],
				['A5','B5','C5','D5','E5','F5'],
				['A6','B6','C6','D6','E6','F6']]
    ordinates =[[[-0.89,0.89,0.15588],[-0.53,0.89,0.15588],[-0.17,0.89,0.15588],[0.19,0.89,0.15588],[0.54,0.89,0.15588],[0.89,0.89,0.15588]],
                [[-0.89,0.53,0.15588],[-0.53,0.53,0.15588],[-0.17,0.53,0.15588],[0.19,0.53,0.15588],[0.54,0.53,0.15588],[0.89,0.53,0.15588]],
                [[-0.89,0.17,0.15588],[-0.53,0.17,0.15588],[-0.17,0.17,0.15588],[0.19,0.17,0.15588],[0.54,0.17,0.15588],[0.89,0.17,0.15588]],
                [[-0.89,-0.19,0.15588],[-0.53,-0.19,0.15588],[-0.17,-0.19,0.15588],[0.19,-0.19,0.15588],[0.54,-0.18,0.15588],[0.89,-0.19,0.15588]],
                [[-0.89,-0.53,0.15588],[-0.53,-0.53,0.15588],[-0.17,-0.53,0.15588],[0.19,-0.53,0.15588],[0.54,-0.53,0.15588],[0.89,-0.53,0.15588]],
                [[-0.89,-0.89,0.15588],[-0.53,-0.89,0.15588],[-0.17,-0.89,0.15588],[0.19,-0.89,0.15588],[0.54,-0.88,0.15588],[0.89,-0.89,0.15588]]]
    for w in range(0,6):
        for x in range(0,6):
            if(nodes[w][x]==start_node):
                sim.setObjectPosition(start,arena,ordinates[w][x])
                model_int=sim.setObjectAlias(start,"Start_Node")
    for w in range(0,6):
        for x in range(0,6):
            if(nodes[w][x]==end_node):
                sim.setObjectPosition(end,arena,ordinates[w][x])
                model_int=sim.setObjectAlias(end,"End_Node")
    all_models.append(start)
    all_models.append(end)
    for i in range(len(all_models)):
        sim.setObjectParent(all_models[i],arena,1)
####################################################################
    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  
####################### ADD YOUR CODE HERE #########################
    hor=[]
    for k in range(len(horizontal_roads_under_construction)):
        horiz=sim.loadModel(horiz_barricade_model)
        hor.append(horiz)
    nodes  =   [['A1-B1','B1-C1','C1-D1','D1-E1','E1-F1'],
				['A2-B2','B2-C2','C2-D2','D2-E2','E2-F2'],
				['A3-B3','B3-C3','C3-D3','D3-E3','E3-F3'],
				['A4-B4','B4-C4','C4-D4','D4-E4','E4-F4'],
				['A5-B5','B5-C5','C5-D5','D5-E5','E5-F5'],
				['A6-B6','B6-C6','C6-D6','D6-E6','E6-F6']]
    nodes_20  =[['A1_B1','B1_C1','C1_D1','D1_E1','E1_F1'],
				['A2_B2','B2_C2','C2_D2','D2_E2','E2_F2'],
				['A3_B3','B3_C3','C3_D3','D3_E3','E3_F3'],
				['A4_B4','B4_C4','C4_D4','D4_E4','E4_F4'],
				['A5_B5','B5_C5','C5_D5','D5_E5','E5_F5'],
				['A6_B6','B6_C6','C6_D6','D6_E6','E6_F6']]
    ordinates =[[[-0.7091,0.8891,0.0255],[-0.3491,0.8891,0.0255],[0,0.8891,0.0255],[0.3591,0.8891,0.0255],[0.7191,0.8891,0.0255]],
                [[-0.7091,0.5391,0.0255],[-0.3491,0.5391,0.0255],[0,0.5391,0.0255],[0.3591,0.5391,0.0255],[0.7191,0.5391,0.0255]],
                [[-0.7091,0.1791,0.0255],[-0.3491,0.1791,0.0255],[0,0.1791,0.0255],[0.3591,0.1791,0.0255],[0.7191,0.1791,0.0255]],
                [[-0.7091,-0.1791,0.0255],[-0.3491,-0.1791,0.0255],[0,-0.1791,0.0255],[0.3591,-0.1791,0.0255],[0.7191,-0.1791,0.0255]],
                [[-0.7091,-0.5391,0.0255],[-0.3491,-0.5391,0.0255],[0,-0.5391,0.0255],[0.3591,-0.5391,0.0255],[0.7191,-0.5391,0.0255]],
                [[-0.7091,-0.8891,0.0255],[-0.3491,-0.8891,0.0255],[0,-0.8891,0.0255],[0.3591,-0.8891,0.0255],[0.7191,-0.8891,0.0255]]]
    co=[]
    co_1=[]
    for i in range(len(horizontal_roads_under_construction)):
        for w in range(0,6):
            for x in range(0,5):
                if(nodes[w][x]==horizontal_roads_under_construction[i]):
                    co.append(ordinates[w][x])
                    co_1.append(nodes_20[w][x])
    for k in range(len(co)):
        sim.setObjectPosition(hor[k],arena,co[k])
    all_models.extend(hor)
    for i in range(len(horizontal_roads_under_construction)):
        model_int=sim.setObjectAlias(hor[i],"Horizontal_missing_road_"+co_1[i])
####################################################################
    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	

	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena')
####################### ADD YOUR CODE HERE #########################
    ver=[]
    for k in range(len(vertical_roads_under_construction)):
        verti=sim.loadModel(vert_barricade_model)
        ver.append(verti)
    nodes =[['F1-F2','F2-F3','F3-F4','F4-F5','F5-F6'],
			['E1-E2','E2-E3','E3-E4','E4-E5','E5-E6'],
			['D1-D2','D2-D3','D3-D4','D4-D5','D5-D6'],
			['C1-C2','C2-C3','C3-C4','C4-C5','C5-C6'],
			['B1-B2','B2-B3','B3-B4','B4-B5','B5-B6'],
		    ['A1-A2','A2-A3','A3-A4','A4-A5','A5-A6']]
    nodes_20 =[['F1_F2','F2_F3','F3_F4','F4_F5','F5_F6'],
			['E1_E2','E2_E3','E3_E4','E4_E5','E5_E6'],
			['D1_D2','D2_D3','D3_D4','D4_D5','D5_D6'],
			['C1_C2','C2_C3','C3_C4','C4_C5','C5_C6'],
			['B1_B2','B2_B3','B3_B4','B4_B5','B5_B6'],
		    ['A1_A2','A2_A3','A3_A4','A4_A5','A5_A6']]
    ordinates =[[[0.8819,0.7131,0.0255],[0.8819,0.3631,0.0255],[0.8819,0,0.0255],[0.8819,-0.3431,0.0255],[0.8819,-0.7031,0.0255]],
                [[0.5319,0.7131,0.0255],[0.5319,0.3631,0.0255],[0.5319,0,0.0255],[0.5319,-0.3431,0.0255],[0.5319,-0.7031,0.0255]],
                [[0.1719,0.7131,0.0255],[0.1719,0.3631,0.0255],[0.1719,0,0.0255],[0.1719,-0.3431,0.0255],[0.1719,-0.7031,0.0255]],
                [[-0.1819,0.7131,0.0255],[-0.1819,0.3631,0.0255],[-0.1819,0,0.0255],[-0.1819,-0.3431,0.0255],[-0.1819,-0.7031,0.0255]],
                [[-0.5391,0.7131,0.0255],[-0.5319,0.3631,0.0255],[-0.5319,0,0.0255],[-0.5319,-0.3431,0.0255],[-0.5319,-0.7031,0.0255]],
                [[-0.8991,0.7131,0.0255],[-0.8991,0.3631,0.0255],[-0.8991,0,0.0255],[-0.8991,-0.3431,0.0255],[-0.8991,-0.7031,0.0255]]]
    co=[]
    co_1=[]
    for i in range(len(vertical_roads_under_construction)):
        for w in range(0,6):
            for x in range(0,5):
                if(nodes[w][x]==vertical_roads_under_construction[i]):
                    co.append(ordinates[w][x])
                    co_1.append(nodes_20[w][x])
    for k in range(len(co)):
        sim.setObjectPosition(ver[k],arena,co[k])
    all_models.extend(ver)
    for i in range(len(vertical_roads_under_construction)):
        model_int=sim.setObjectAlias(ver[i],"Vertical_missing_road_"+co_1[i])
####################################################################
    return all_models

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    # path directory of images in test_images folder
    img_dir = os.getcwd() + "\\Downloads\\PB Task 4A\\PB Task 4A\\test_imgs\\"

    i = 0
    config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

    print('\n============================================')
    print('\nFor maze_0.png')

    # object handles of each model that gets imported to the scene can be stored in this list
    # at the end of each test image, all the models will be removed    
    all_models = []

    # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
    task_1 = __import__('task_1a')
    detected_arena_parameters = task_1.detect_arena_parameters(config_img)

    # obtain required arena parameters
    medicine_package_details = detected_arena_parameters["medicine_packages"]
    traffic_signals = detected_arena_parameters['traffic_signals']
    start_node = detected_arena_parameters['start_node']
    end_node = detected_arena_parameters['end_node']
    horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
    vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

    print("[1] Setting up the scene in CoppeliaSim")
    all_models = place_packages(medicine_package_details, sim, all_models)
    all_models = place_traffic_signals(traffic_signals, sim, all_models)
    all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
    all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
    all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
    print("[2] Completed setting up the scene in CoppeliaSim")

    # wait for 10 seconds and then remove models
    time.sleep(10)
    print("[3] Removing models for maze_0.png")
    for i in all_models:
        sim.removeModel(i)

   
    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
    
    if choice == 'y':
        for i in range(1,5):

            print('\n============================================')
            print('\nFor maze_' + str(i) +'.png')
            config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

            # object handles of each model that gets imported to the scene can be stored in this list
            # at the end of each test image, all the models will be removed    
            all_models = []

            # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
            task_1 = __import__('task_1a')
            detected_arena_parameters = task_1.detect_arena_parameters(config_img)

            # obtain required arena parameters
            medicine_package_details = detected_arena_parameters["medicine_packages"]
            traffic_signals = detected_arena_parameters['traffic_signals']
            start_node = detected_arena_parameters['start_node']
            end_node = detected_arena_parameters['end_node']
            horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
            vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

            print("[1] Setting up the scene in CoppeliaSim")
            place_packages(medicine_package_details, sim, all_models)
            place_traffic_signals(traffic_signals, sim, all_models)
            place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
            place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
            place_start_end_nodes(start_node, end_node, sim, all_models)
            print("[2] Completed setting up the scene in CoppeliaSim")
            # wait for 10 seconds and then remove models
            time.sleep(10)
            print("[3] Removing models for maze_" + str(i) + '.png')
            for i in all_models:
                sim.removeModel(i)
            