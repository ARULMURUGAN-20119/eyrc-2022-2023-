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

# Team ID:			[ PB_1915 ]
# Author List:		[ Arulmurugan T,Anbarasu R,Akshay Raj A V,Aditya S M ]
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
from itertools import count
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





##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

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
	j1=sim.getObject('/left_joint')
	j2=sim.getObject('/right_joint')	
	l=0.2
	sim.setJointTargetVelocity(j1,l)
	sim.setJointTargetVelocity(j2,l)
	p=0.0005
	point='A'
	package={'Orange Cone':'package_1','Blue Cylinder':'package_2','Pink Cuboid':'package_3'}
	while(1):
		# a,b,c= sim.readVisionSensor(sim.getObject('/vision_sensor'))
		# time.sleep(0.1)
		#print(c[1])
		#k=round(b[11],2)
		#print(k)
		g,j=sim.getVisionSensorImg(sim.getObject('/vision_sensor'))
		##print(g)
		# np.frombuffer(g,dtype=np.unit8)
		s1=np.reshape(np.frombuffer(g,dtype=np.uint8),(512,512,3)).tolist()
		# print(np.shape(s1))
		print(s1[0][0],s1[0][-1],s1[-1][0],s1[-1][-1])
		s3=s1[-1][:64]
		s4=s1[-1][(512-64):512]
		corr=(s3.count([255,255,255])-s4.count([255,255,255]))*p
		sim.setJointTargetVelocity(j1,l+corr)
		sim.setJointTargetVelocity(j2,l-corr)
		print(s3.count([255,255,255]),s4.count([255,255,255]),corr)
		qr_message = None
		if (s1[0][0],s1[0][-1])!=([255, 255, 255], [255, 255, 255]):
			sim.setJointTargetVelocity(j1,0)
			sim.setJointTargetVelocity(j2,0)
			
			## Retrieve the handle of the Arena_dummy scene object.
			arena_dummy_handle = sim.getObject("/Arena_dummy") 

			## Retrieve the handle of the child script attached to the Arena_dummy scene object.
			childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

			## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint 
			point1='checkpoint '+point
			print('Current',point1)
			sim.callScriptFunction("activate_qr_code", childscript_handle, point1)
			qr_message = read_qr_code(sim)
			print('Decoded Qr message',qr_message)
			## Retrieve the handle of the Arena_dummy scene object.
			arena_dummy_handle = sim.getObject("/Arena_dummy") 

			## Retrieve the handle of the child script attached to the Arena_dummy scene object.
			childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

			## Call the deactivate_qr_code() function defined in the child script to make the QR code invisible at checkpoint E
			sim.callScriptFunction("deactivate_qr_code", childscript_handle, point1)
			point=chr(ord(point)+1)
			time.sleep(2)
			break
	l=0.5
	sim.setJointTargetVelocity(j1,l)
	sim.setJointTargetVelocity(j2,l)
	time.sleep(1.55)
	o1=sim.getObjectOrientation(sim.getObject('/Diff_Drive_Bot'),sim.getObject('/Arena'))
	print(o1)
	o1[0]+=(22/7)/2
	sim.setObjectOrientation(sim.getObject('/Diff_Drive_Bot'),sim.getObject('/Arena'),o1)
	
	l=0
	sim.setJointTargetVelocity(j1,-l)
	sim.setJointTargetVelocity(j2,l)
	time.sleep(1)

	count=0
	while True:
		l=0.2
		sim.setJointTargetVelocity(j1,l)
		sim.setJointTargetVelocity(j2,l)
		qr_message=None
		while(1):
			# a,b,c= sim.readVisionSensor(sim.getObject('/vision_sensor'))
			# time.sleep(0.1)
			#print(c[1])
			#k=round(b[11],2)
			#print(k)
			g,j=sim.getVisionSensorImg(sim.getObject('/vision_sensor'))
			##print(g)
			# np.frombuffer(g,dtype=np.unit8)
			s1=np.reshape(np.frombuffer(g,dtype=np.uint8),(512,512,3)).tolist()
			# print(np.shape(s1))
			print(s1[0][0],s1[0][-1],s1[-1][0],s1[-1][-1])
			s3=s1[-1][:64]
			s4=s1[-1][(512-64):512]
			corr=(s3.count([255,255,255])-s4.count([255,255,255]))*p
			sim.setJointTargetVelocity(j1,l+corr)
			sim.setJointTargetVelocity(j2,l-corr)
			print(s3.count([255,255,255]),s4.count([255,255,255]),corr)
			qr_message = None
			if s1[0][0]!=[255, 255, 255] and s1[0][-1]!=[255, 255, 255]:
				sim.setJointTargetVelocity(j1,0)
				sim.setJointTargetVelocity(j2,0)
				
				## Retrieve the handle of the Arena_dummy scene object.
				arena_dummy_handle = sim.getObject("/Arena_dummy") 

				## Retrieve the handle of the child script attached to the Arena_dummy scene object.
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

				## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint 
				point1='checkpoint '+point
				print('Current',point1)
				sim.callScriptFunction("activate_qr_code", childscript_handle, point1)
				qr_message = read_qr_code(sim)
				print('Decoded Qr message',qr_message)
				## Retrieve the handle of the Arena_dummy scene object.
				arena_dummy_handle = sim.getObject("/Arena_dummy") 

				## Retrieve the handle of the child script attached to the Arena_dummy scene object.
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

				## Call the deactivate_qr_code() function defined in the child script to make the QR code invisible at checkpoint E
				sim.callScriptFunction("deactivate_qr_code", childscript_handle, point1)
				point=chr(ord(point)+1)
				time.sleep(2)
				break
		l=0.5
		sim.setJointTargetVelocity(j1,l)
		sim.setJointTargetVelocity(j2,l)
		time.sleep(1.55)
		if qr_message==None:
			o1=sim.getObjectOrientation(sim.getObject('/Diff_Drive_Bot'),sim.getObject('/Arena'))
			print(o1)
			angle=(22/7)/2
			if count%3==1:
				angle=-angle
			
			o1[0]-=angle
			sim.setObjectOrientation(sim.getObject('/Diff_Drive_Bot'),sim.getObject('/Arena'),o1)
			count+=1
		else:
			#pakage dropping and breaking
			## Retrieve the handle of the Arena_dummy scene object.
			arena_dummy_handle = sim.getObject("/Arena_dummy") 

			## Retrieve the handle of the child script attached to the Arena_dummy scene object.
			childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

			## Deliver package_1 at checkpoint E
			sim.callScriptFunction("deliver_package", childscript_handle, package[qr_message], point1)
			#package+=1
			pass
		l=0
		sim.setJointTargetVelocity(j1,-l)
		sim.setJointTargetVelocity(j2,l)
		time.sleep(1)

	
	# ##################################################

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	##############  ADD YOUR CODE HERE  ##############
	
	g,j=sim.getVisionSensorImg(sim.getObject('/vision_sensor'))
	image=np.reshape(np.frombuffer(g,dtype=np.uint8),(512,512,3))
	k=decode(image) 
	for i in k:
		qr_message=i[0].decode("utf-8")

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
			#time.sleep(0.5)
			control_logic(sim)

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