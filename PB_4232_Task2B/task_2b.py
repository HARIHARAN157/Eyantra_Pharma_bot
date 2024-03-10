'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
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
# Author List:		[ HARIHARAN S ,PARTHIBAN V ,AJAY PRANAV P R ,MAVEENKUMAR S]
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def yellow(img):
		low = np.uint8([50,210,255])
		high = np.uint8([0,0,0])
		masks = cv2.inRange(img, high, low)
		contour, hierarchy = cv2.findContours(masks, 3, cv2.CHAIN_APPROX_NONE)
		if len(contour) > 0 :
			d = max(contour, key=cv2.contourArea)
			N = cv2.moments(d)
			if N["m00"] !=0 :
				dx = int(N['m10']/N['m00'])
				dy = int(N['m01']/ N['m00'])
			cv2.drawContours(img, d, -1, (0,0,255), 3)
			return (dx,dy)
def turn_left(lmotor,rmotor,sim):

	sim.setJointTargetVelocity(lmotor,1.2)
	sim.setJointTargetVelocity(rmotor,1.2)
	time.sleep(0.4)
	sim.setJointTargetVelocity(lmotor,-1.8)
	sim.setJointTargetVelocity(rmotor,1.8)
	time.sleep(0.5)
def turn_right(lmotor,rmotor,sim):
	sim.setJointTargetVelocity(rmotor,1.2)
	sim.setJointTargetVelocity(lmotor,1.2)
	time.sleep(0.4)
	sim.setJointTargetVelocity(rmotor,-1.8)
	sim.setJointTargetVelocity(lmotor,1.8)
	time.sleep(0.5)
def deliveryE(sim,P):
	if(P=='Orange Cone'):
		A="package_1"
	elif(P=='Blue Cylinder'):
		A="package_2"
	else:
		A="package_3"
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deliver_package", childscript_handle,A, "checkpoint E")
def deliveryI(sim,P):
	if(P=='Orange Cone'):
		A="package_1"
	elif(P=='Blue Cylinder'):
		A="package_2"
	else:
		A="package_3"
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deliver_package", childscript_handle, A, "checkpoint I")
def deliveryM(sim,P):
	if(P=='Orange Cone'):
		A="package_1"
	elif(P=='Blue Cylinder'):
		A="package_2"
	else:
		A="package_3"
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deliver_package", childscript_handle,A, "checkpoint M")
##############################################################

def control_logic(sim):

		##############  ADD YOUR CODE HERE  ##############

	lmotor = sim.getObjectHandle("./left_joint")
	rmotor = sim.getObjectHandle("./right_joint")
	a=0
	b=0
	while(True):
		sensor =sim.getObjectHandle('./vision_sensor')
		img, resX, resY = sim.getVisionSensorCharImage(sensor)
		img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
		img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
		low_b = np.uint8([180,230,255])
		high_b = np.uint8([0,0,0])
		mask = cv2.inRange(img, high_b, low_b)
		contours, hierarchy = cv2.findContours(mask, 3, cv2.CHAIN_APPROX_NONE)
		dy = yellow(img)
		if len(contours) > 0 :
			c = max(contours, key=cv2.contourArea)
			M = cv2.moments(c)
			if M["m00"] !=0 :
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				cv2.drawContours(img, c, -1, (0,255,0), 3)
				if(cx>250 and cx<265 and dy == None):
					sim.setJointTargetVelocity(lmotor,2.9)
					sim.setJointTargetVelocity(rmotor,2.9)
				elif(cx<=250) and dy==None:
					sim.setJointTargetVelocity(lmotor,0)
					sim.setJointTargetVelocity(rmotor,0.5)			
				elif(cx>=265 and dy== None):
					sim.setJointTargetVelocity(lmotor,0.5)
					sim.setJointTargetVelocity(rmotor,0)
				elif(500>dy[1]):
					if(dy[0]>254 and dy[0]<265 and dy[1]<200):
							sim.setJointTargetVelocity(lmotor,0.5)
							sim.setJointTargetVelocity(rmotor,0.5)
					elif(dy[0]<=254 and dy[1]<200):
							sim.setJointTargetVelocity(lmotor,0)
							sim.setJointTargetVelocity(rmotor,0.3)			
					elif(dy[0])>=265 and dy[1]<200:
							sim.setJointTargetVelocity(lmotor,0.3)
							sim.setJointTargetVelocity(rmotor,0)
					elif(dy[1]>200):
						if(a==0):
							turn_left(lmotor,rmotor,sim)
							a=a+1
						elif(a==1):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==2):
							turn_left(lmotor,rmotor,sim)
							a=a+1
						elif(a==3):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==4):
							arena_dummy_handle = sim.getObject("/Arena_dummy") 
							childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
							sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint E")
							if(dy[1]>230):
									if(b==0):
										P=read_qr_code(sim)
										time.sleep(1)
										arena_dummy_handle = sim.getObject("/Arena_dummy") 
										childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
										sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint E")
										deliveryE(sim,P)
										b=1
										sim.setJointTargetVelocity(lmotor,0.9)
										sim.setJointTargetVelocity(rmotor,0.9)

							if(dy[1]>450):	
								a=a+1
						elif(a==5):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==6):
							turn_left(lmotor,rmotor,sim)
							a=a+1
						elif(a==7):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==8):
							arena_dummy_handle = sim.getObject("/Arena_dummy") 
							childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
							sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint I")
							if(dy[1]>200):
								arena_dummy_handle = sim.getObject("/Arena_dummy") 
								childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
								sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint I")
								if(dy[1]>240):
									if(b==1):
										P=read_qr_code(sim)
										time.sleep(1)
										arena_dummy_handle = sim.getObject("/Arena_dummy") 
										childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
										sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint I")
										deliveryI(sim,P)
										b=2
										sim.setJointTargetVelocity(lmotor,0.9)
										sim.setJointTargetVelocity(rmotor,0.9)
							if(dy[1]>420):	
								a=a+1
						elif(a==9):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==10):
							turn_left(lmotor,rmotor,sim)
							a=a+1
						elif(a==11):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==12):
							if(dy[1]>230):
								arena_dummy_handle = sim.getObject("/Arena_dummy") 
								childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
								sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint M")
								if(dy[1]>260):
									if(b==2):
										P=read_qr_code(sim)
										time.sleep(1)
										arena_dummy_handle = sim.getObject("/Arena_dummy") 
										childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
										sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint M")
										deliveryM(sim,P)
										b=3
										sim.setJointTargetVelocity(lmotor,0.8)
										sim.setJointTargetVelocity(rmotor,0.8)
							if(dy[1]>450):	
								a=a+1
						elif(a==13):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==14):
							turn_left(lmotor,rmotor,sim)
							a=a+1
						elif(a==15):
							turn_right(lmotor,rmotor,sim)
							a=a+1
						elif(a==16):
							sim.setJointTargetVelocity(lmotor,2.3)
							sim.setJointTargetVelocity(rmotor,2.3)
							time.sleep(0.25)
							sim.setJointTargetVelocity(lmotor,0)
							sim.setJointTargetVelocity(rmotor,0)
							break
		##################################################

def read_qr_code(sim):

		qr_message = None

	##############  ADD YOUR CODE HERE  ##############
		sensor =sim.getObjectHandle('./vision_sensor')
		img, resX, resY = sim.getVisionSensorCharImage(sensor)
		img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
		img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
		result = decode(img)
		qr_message = result[0][0].decode()
	##################################################
		return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			control_logic(sim)
			time.sleep(5)
		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		
		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()
