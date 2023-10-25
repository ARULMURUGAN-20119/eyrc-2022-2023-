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
*  Filename:			task_2a.py
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

# Team ID:			[PB_1915]
# Author List:		[ Arulmurugan T,Anbarasu R,Akshay Raj A V,Aditya S M ]
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
from dis import dis
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""
	##############  ADD YOUR CODE HERE  ##############
	count=0
	j1=sim.getObject('/left_joint')
	j2=sim.getObject('/right_joint')
	sim.setJointTargetVelocity(j1,2)
	sim.setJointTargetVelocity(j2,2)
	while True:
		count+=1
		j1=sim.getObject('/left_joint')
		j2=sim.getObject('/right_joint')

		
		while(1):
			k=detect_distance_sensor_1(sim)
			
			

			if k!=None:
				k=round(k,2)
				print(k)
				if k<=0.18:
					break
			f=detect_distance_sensor_2(sim)
			if f!=None:
				f=round(f,2)
				if f==0.18:
					sim.setJointTargetVelocity(j1,1)
					sim.setJointTargetVelocity(j2,1)
					continue
				d=0.1
				if f>0.18:
					d=-d
				
				l=sim.getJointTargetVelocity(j1)
				print('f===',f,d, l,l+d)
				sim.setJointTargetVelocity(j1,l)
				sim.setJointTargetVelocity(j2,l+d)
		
		if detect_distance_sensor_2(sim)==None:
			j1,j2=j2,j1
		l=sim.getJointTargetVelocity(j1)
		sim.setJointTargetVelocity(j1,-l)
		sim.setJointTargetVelocity(j2,l)
		# time.sleep(2.2)
		if count==1:
			time.sleep(2.2)
		if count==2:
			time.sleep(2.2)
		if count==3:
			time.sleep(2.2)
		if count==4:
			time.sleep(2.2)
		if count==5:
			time.sleep(2.2)
		if count==6:
			time.sleep(2.3)
		if count==7:
			time.sleep(2.3)
		if count==8:
			time.sleep(2.3)
		if count==9:
			time.sleep(2.3)
		if count==10:
			sim.setJointTargetVelocity(j1,0)
			sim.setJointTargetVelocity(j2,0)
			break

		
		sim.setJointTargetVelocity(j1,l)
		sim.setJointTargetVelocity(j2,l)

	##################################################

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
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	sensor1=sim.getObject('/distance_sensor_1')
	result,distance1,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.readProximitySensor(sensor1)
	if result==1:
		distance=distance1
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

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	sensor1=sim.getObject('/distance_sensor_2')
	result,distance1,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.readProximitySensor(sensor1)
	if result==1:
		distance=distance1
	
	

		# import time
		#time.sleep(1)
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