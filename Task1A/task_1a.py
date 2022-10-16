'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ PB-1915 ]
# Author List:		[Arulmurugan T,Anbarasu R,Akshay Raj A V,Aditya S M ]
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def f(l):
	#print(l,ord(l[1][0]))
	return ord(l[1][0])




##############################################################

def detect_traffic_signals(maze_image):

	"""
    Purpose:
    ---
    This function takes the image as an argument and returns a list of
    nodes in which traffic signals are present in the image

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `traffic_signals` : [ list ]
            list containing nodes in which traffic signals are present

    Example call:
    ---
    traffic_signals = detect_traffic_signals(maze_image)
    """
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############

	maze_images=maze_image.tolist()
	for i in range(100,800,100):

		for j in range(100,800,100):
			#print(maze_images[i][j],end='')
			if maze_images[i][j]==[0, 0, 255]:

				traffic_signals.append(chr(65-1+int(j/100))+str(int(i/100)))

	##################################################
	#print('\n',traffic_signals)
	return traffic_signals


def detect_horizontal_roads_under_construction(maze_image):

	"""
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing horizontal links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `horizontal_roads_under_construction` : [ list ]
            list containing missing horizontal links

    Example call:
    ---
    horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
    """
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	maze_images=maze_image.tolist()
	for i in range(100,800,100):
		for j in range(150,700,100):
			#print(maze_images[i][j],end='')
			if maze_images[i][j]==[255, 255, 255]:

				horizontal_roads_under_construction.append(chr(64+int(j/100))+str(int(i/100))+'-'+chr(65+int(j/100))+str(int(i/100)))


	##################################################

	return horizontal_roads_under_construction

def detect_vertical_roads_under_construction(maze_image):

	"""
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing vertical links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `vertical_roads_under_construction` : [ list ]
            list containing missing vertical links

    Example call:
    ---
    vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
    """
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	maze_images=maze_image.tolist()
	for i in range(150,700,100):
		#print('\n')
		for j in range(100,800,100):
			#print(maze_images[i][j],end='')
			if maze_images[i][j]==[255, 255, 255]:

				vertical_roads_under_construction.append(chr(64+int(j/100))+str(int(i/100))+'-'+chr(64+int(j/100))+str(int(i/100)+1))
	##################################################

	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

	"""
    Purpose:
    ---
    This function takes the image as an argument and returns a nested list of
    details of the medicine packages placed in different shops

    ** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers
       as well as in the alphabetical order of colors.
       For example, the list should first have the packages of shop_1 listed.
       For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `medicine_packages` : [ list ]
            nested list containing details of the medicine packages present.
            Each element of this list will contain
            - Shop number as Shop_n
            - Color of the package as a string
            - Shape of the package as a string
            - Centroid co-ordinates of the package
    Example call:
    ---
    medicine_packages = detect_medicine_packages(maze_image)
    """
	medicine_packages = []

	##############	ADD YOUR CODE HERE	##############
	# from matplotlib import pyplot as plt
	for j in range(1,7):
		d = 10
		img = maze_image[100+d:200-d,(j*100)+d:((j+1)*100)-d]





		# converting image into grayscale image
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# setting threshold of gray image
		_, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

		# using a findContours() function
		contours, _ = cv2.findContours(
			threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		i = 0
		l=[]

		# list for storing names of shapes
		for contour in contours:

			# here we are ignoring first counter because
			# findcontour function detects whole image as shape
			if i == 0:
				i = 1
				continue

			# cv2.approxPloyDP() function to approximate the shape
			approx = cv2.approxPolyDP(
				contour, 0.01 * cv2.arcLength(contour, True), True)

			# using drawContours() function
			# cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

			# finding center point of shape
			M = cv2.moments(contour)
			if M['m00'] != 0.0:
				x = int(M['m10']/M['m00'])+ (j*100)+d
				y = int(M['m01']/M['m00'])+ 100+d

			# putting shape name at center of each shape

			maze_images=maze_image.tolist()
			mat=maze_images[y][x]
			#print(mat)
			color=''
			if mat== [255, 255,   0]:
				color='Skyblue'
			elif mat==[  0 ,127, 255]:
				color='Orange'
			elif mat==[180  , 0 ,255]:
				color='Pink'
			elif mat==[0,255,0]:
				color='Green'
			if len(approx) == 5:
				l.append(['Shop_'+str(j),color,'Triangle', [x, y]])
			elif len(approx) == 8:
				l.append(['Shop_'+str(j),color,'Square', [x, y]])
			else:
				l.append(['Shop_'+str(j),color,'circle', [x, y]])
		if len(l)>0:
			l=sorted(l,key=f)
			#print(l)
			medicine_packages.append(l)
		# cv2.imshow('shapes', img)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):

	"""
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary
    containing the details of the different arena parameters in that image

    The arena parameters are of four categories:
    i) traffic_signals : list of nodes having a traffic signal
    ii) horizontal_roads_under_construction : list of missing horizontal links
    iii) vertical_roads_under_construction : list of missing vertical links
    iv) medicine_packages : list containing details of medicine packages

    These four categories constitute the four keys of the dictionary

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `arena_parameters` : { dictionary }
            dictionary containing details of the arena parameters

    Example call:
    ---
    arena_parameters = detect_arena_parameters(maze_image)
    """
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena_parameters = {'traffic_signals':detect_traffic_signals(maze_image),'horizontal_roads_under_construction':detect_horizontal_roads_under_construction(maze_image),'vertical_roads_under_construction':detect_vertical_roads_under_construction(maze_image),'medicine_packages_present':detect_medicine_packages(maze_image)}
	##################################################

	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########

if __name__ == "__main__":

	# path directory of images in test_images folder
	img_dir_path = "public_test_images/"

	# path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'

	# read image using opencv
	maze_image = cv2.imread(img_file_path)


	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 15):

			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'

			# read image using opencv
			maze_image = cv2.imread(img_file_path)

			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')

			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)

			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()