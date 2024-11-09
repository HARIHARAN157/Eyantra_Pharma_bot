'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 4B of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_4b.py
# Functions:		
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import threading
import time
import os, sys
from zmqRemoteApi import RemoteAPIClient
import traceback
import zmq
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
import random
##############################################################

## Import PB_theme_functions code
color=[]
path = __import__('task_3a')
task_1b = __import__('task_1b')
try:
	pb_theme = __import__('PB_theme_functions')

except ImportError:
	print('\n[ERROR] PB_theme_functions.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure PB_theme_functions.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your PB_theme_functions.py throwed an Exception, kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()
def task_4b_implementation(sim,image):
	"""
	Purpose:
	---
	This function contains the implementation logic for task 4B 

	Input Arguments:
	---
    `sim` : [ object ]
            ZeroMQ RemoteAPI object

	You are free to define additional input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	task_4b_implementation(sim)
	"""

	##################	ADD YOUR CODE HERE	##################
	paths_1=path.detect_arena_parameters(image)
	traffic_signal=paths_1["traffic_signals"]
	start_nodes=paths_1["start_node"]
	end_nodes=paths_1["end_node"]
	paths=paths_1["paths"]
	medicine_package_details = detected_arena_parameters["medicine_packages"]
	for i in range(len(medicine_package_details)):
		if(medicine_package_details[i][0]=='Shop_1'):
			end_nodes='B2'
		elif(medicine_package_details[i][0]=='Shop_2'):
			end_nodes='C2'
		elif(medicine_package_details[i][0]=='Shop_3'):
			end_nodes='D2'
		elif(medicine_package_details[i][0]=='Shop_4'):
			end_nodes='E2'
		elif(medicine_package_details[i][0]=='Shop_5'):
			end_nodes='F2'
	back_path= path.path_planning(paths,start_nodes,end_nodes)
	moves=path.paths_to_moves(back_path,traffic_signal)
	moves.append("Stop")
	for i in range(len(moves)):
		pb_theme.send_message_via_socket(connection_2, moves[i])
		time.sleep(1)
		print(moves[i])
	while(True):
		print('a')
		message = pb_theme.receive_message_via_socket(connection_2)
		if(message=="Arrived"):
			print('a')
			break
	qr = cv2.imread(r"C:\Users\HARI\Downloads\PB_Task4B_Windows\PB_Task4B_Windows\qr_drop_5.png")
	cor=task_1b.detect_Qr_details(qr)
	pb_theme.send_message_via_socket(connection_2, cor)	
'''	colour(30,medicine_package_details)
def colour(qr_handle,medicine_package_details):
	for i in range(len(medicine_package_details)):
		color.append(medicine_package_details[i][0])
	pb_theme.send_message_via_socket(connection_2,color)'''
	##########################################################
def simu(transform,sim):
	video = cv2.VideoCapture(0)
	c=0;d=0;e=0;f=0
#qr=sim.getObject("/qr_plane")
#	sim.setObjectPosition(22,15,[-0.8880,-0.4119,0.0445])
#	sim.setObjectInt32Param(qr,[-0.89,-5340,0.0021])
	while(True):
		_, frame = video.read()
		cv2.imshow('frame',frame)
		cv2.waitKey(1)
		warped_image,c,d,e,f=transform.perspective_transform(frame,c,d,e,f)
		scene_parameters=transform.transform_values(warped_image)
		transform.set_values(sim,scene_parameters)


if __name__ == "__main__":
	host = '192.168.43.154'
	port = 5050


	## Set up new socket server
	try:
		server = pb_theme.setup_server(host, port)
		print("Socket Server successfully created")

		# print(type(server))

	except socket.error as error:
		print("Error in setting up server")
		print(error)
		sys.exit()


	## Set up new connection with a socket client (PB_task3d_socket.exe)
	try:
		print("\nPlease run PB_socket.exe program to connect to PB_socket client")
		connection_1, address_1 = pb_theme.setup_connection(server)
		print("Connected to: " + address_1[0] + ":" + str(address_1[1]))

	except KeyboardInterrupt:
		sys.exit()

	# ## Set up new connection with Raspberry Pi
	try:
		print("\nPlease connect to Raspberry pi client")
		connection_2, address_2 = pb_theme.setup_connection(server)
		print("Connected to: " + address_2[0] + ":" + str(address_2[1]))

	except KeyboardInterrupt:
		sys.exit()
	pb_theme.send_message_via_socket(connection_1,"SETUP")

	message=pb_theme.receive_message_via_socket(connection_1)
	## Loop infinitely until SETUP_DONE message is received
	while True:
		if message == "SETUP_DONE":
			break
		else:
			print("Cannot proceed further until SETUP command is received")
			message = pb_theme.receive_message_via_socket(connection_1)

	try:
		# obtain required arena parameters
		config_img = cv2.imread(r"C:\Users\HARI\Downloads\PB_Task4B_Windows\PB_Task4B_Windows\config_image.png")
		
		detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)
		medicine_package_details = detected_arena_parameters["medicine_packages"]
		traffic_signals = detected_arena_parameters['traffic_signals']
		start_node = detected_arena_parameters['start_node']
		end_node = detected_arena_parameters['end_node']
		horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
		vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction']
		# print("Medicine Packages: ", medicine_packag	e_details)
		# print("Traffic Signals: ", traffic_signals)
		# print("Start Node: ", start_node)
		# print("End Node: ", end_node)
		# print("Horizontal Roads under Construction: ", horizontal_roads_under_construction)
		# print("Vertical Roads under Construction: ", vertical_roads_under_construction)
		# print("\n\n")
	except Exception as e:
		print('Your task_1a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	try:

		## Connect to CoppeliaSim arena        
		coppelia_client = RemoteAPIClient()
		sim = coppelia_client.getObject('sim')

		## Define all models
		all_models = []

		## Setting up coppeliasim scene
		print("[1] Setting up the scene in CoppeliaSim")
		all_models = pb_theme.place_packages(medicine_package_details, sim, all_models)
		all_models = pb_theme.place_traffic_signals(traffic_signals, sim, all_models)
		all_models = pb_theme.place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_start_end_nodes(start_node, end_node, sim, all_models)
		print("[2] Completed setting up the scene in CoppeliaSim")
		print("[3] Checking arena configuration in CoppeliaSim")

	except Exception as e:
		print('Your task_4a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	pb_theme.send_message_via_socket(connection_1, "CHECK_ARENA")

	## Check if arena setup is ok or not
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		

		if message == "ARENA_SETUP_OK":
			print("[4] Arena was properly setup in CoppeliaSim")
			break
		elif message == "ARENA_SETUP_NOT_OK":
			print("[4] Arena was not properly setup in CoppeliaSim")
			connection_1.close()
			# connection_2.close()
			server.close()
			sys.exit()
		else:
			pass
	## Send Start Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_START")
	
	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STARTED_CORRECTLY":
			print("[5] Simulation was started in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STARTED_CORRECTLY":
			print("[5] Simulation was not started in CoppeliaSim")
			sys.exit()

	## Send Start Command to Raspberry Pi to start execution
	pb_theme.send_message_via_socket(connection_2, "START")
	transform= __import__('task_3c')
	sim_thread = threading.Thread(target=simu, args=(transform, sim))
	sim_thread.start()
	task_4b_implementation(sim,config_img)

	## Send Stop Simulation Command to PB_Socket
	#pb_theme.send_message_via_socket(connection_1, "SIMULATION_STOP")

	## Check if simulation started correctly
	#message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STOPPED_CORRECTLY":
			print("[6] Simulation was stopped in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STOPPED_CORRECTLY":
			print("[6] Simulation was not stopped in CoppeliaSim")
			sys.exit()