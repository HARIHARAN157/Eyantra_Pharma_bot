'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:            task_2a.py
*  Created:             
*  Last Modified:       8/10/2022
*  Author:              e-Yantra Team
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:          [ PB_4232 ]
# Author List:      [ HARIHARAN S,PARTHIBAN V,AJAY PRANAV P R,MAVEENKUMAR S ]
# Filename:         task_2a.py
# Functions:        control_logic, detect_distance_sensor_1, detect_distance_sensor_2
#                   [ Comma separated list of functions in this file ]
# Global variables: 
#                   [ List of global variables defined in this file ]

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
##############################################################

def control_logic(sim):
	timeout = time.time() + 60*0.3
	lmotor = sim.getObjectHandle("./left_joint")
	rmotor = sim.getObjectHandle("./right_joint")
	while(time.time() < timeout):
		distance_1 = detect_distance_sensor_1(sim)
		distance_2 = detect_distance_sensor_2(sim)
		if(distance_1==-1 and distance_2<0.217):
			sim.setJointTargetVelocity(lmotor,5)
			sim.setJointTargetVelocity(rmotor,5)
		elif(0.1<distance_1<0.27 and distance_2!=-1):
			sim.setJointTargetVelocity(lmotor,-2)
			sim.setJointTargetVelocity(rmotor,2)
			time.sleep(0.202)
		elif(distance_2==-1 and 0.1<distance_1<0.21):
			sim.setJointTargetVelocity(lmotor,2)
			sim.setJointTargetVelocity(rmotor,-2)
			time.sleep(0.25)

def detect_distance_sensor_1(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

    Input Arguments:
    ---
    `sim`    :   [ object ]
        ZeroMQ RemoteAPI object

    Returns:
    ---
    distance  :  [ float ]
        distance of obstacle from sensor
    Example call:
    ---
    distance_1 = detect_distance_sensor_1(sim)
    """
    distance = None ##############  ADD YOUR CODE HERE  ##############
    sensorLS =sim.getObjectHandle('./distance_sensor_1')
    distance = sim.readProximitySensor(sensorLS)
    if (distance[3]==-1):
        distance=-1
    else:
        distance=distance[1]
    ##################################################
    return distance

def detect_distance_sensor_2(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

    Input Arguments:
    ---
    `sim`    :   [ object ]
        ZeroMQ RemoteAPI object
    Returns
    ---
    distance  :  [ float ]
        distance of obstacle from sensor

    Example call:
    ---
    distance_2 = detect_distance_sensor_2(sim)
    """

    distance = None
    ##############  ADD YOUR CODE HERE  ##############

    sensorLF=sim.getObjectHandle('./distance_sensor_2')
    distance=sim.readProximitySensor(sensorLF)
    if (distance[3]==-1):
        distance=-1
    else:
        distance=distance[1]
    ##################################################
    return distance

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
            time.sleep(40)

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