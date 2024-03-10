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

# Team ID:			[ PB_4232 ]
# Author List:		[ HARIHARAN S,PARTHIBAN V,AJAY PRANAV P R,MAVEENKUMAR S]
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

def loop(colour,detected_output):
		row = 0
		colm = 0
		i = 0
		j = 0
		k = 0
		nodes =[['A1','B1','C1','D1','E1','F1'],
				['A2','B2','C2','D2','E2','F2'],
				['A3','B3','C3','D3','E3','F3'],
				['A4','B4','C4','D4','E4','F4'],
				['A5','B5','C5','D5','E5','F5'],
				['A6','B6','C6','D6','E6','F6']]
		Arena_list=[]
		for i in range(1,63):
			for j in range(1,63):
				for k in range(1,3):
					if (detected_output[i][j][k]==colour):
						row = int((i/8)-1);colm = int((j/8)-1)
						Arena_list.append(nodes[row][colm])
		return Arena_list	
def output(maze_image,colour):
	maze_image = cv2.resize(maze_image,(63,63))
	upper_red= np.array(colour, dtype = "uint8")
	lower_red= np.array(colour, dtype = "uint8")
	mask = cv2.inRange(maze_image,lower_red,upper_red)
	detected_output = cv2.bitwise_and(maze_image, maze_image, mask =  mask)
	return detected_output



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
	traffic_signals = []
	start_node = ""
	end_node = ""
	purple=[189, 43, 105]
	green =[0, 255, 0]
	red   =[0, 0, 255]
	detected_output=output(maze_image,green)
	start_node =loop(255,detected_output)
	start_node =start_node[-1]
	detected_output=output(maze_image,purple)
	end_node =loop(105,detected_output)
	end_node =end_node[-1]
	detected_output=output(maze_image,red)
	traffic_signals = loop(255,detected_output)
	traffic_signals.sort()	
	return traffic_signals,start_node,end_node
	##################################################

	
	
	

def detect_horizontal_roads_under_construction(maze_image):
	
	"""
	Purpose:,,7
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
	node =[['A1','B1','C1','D1','E1','F1'],
	        ['A2','B2','C2','D2','E2','F2'],
			['A3','B3','C3','D3','E3','F3'],
			['A4','B4','C4','D4','E4','F4'],
			['A5','B5','C5','D5','E5','F5'],
			['A6','B6','C6','D6','E6','F6']]
	res = 10
	resw=10
	row = 0
	colm = 0
	i = 0
	j = 0
	gray = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (3,3), 0)
	thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
	horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
	horizontal_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
	horizontal_mask = cv2.dilate(horizontal_mask, horizontal_kernel, iterations=9)
	result = horizontal_mask-thresh
	result = result[0:606, 106:594]
	result = cv2.resize(result,(50,60))
	for i in range(1,60):
		for j in range(1,50):
			if (result[i][j]==255):
				if(j!=9 and j!=30 and j!=19 and j!=40):
					row=int(i/10);colm=int(j/10)
					if(colm!=res or resw!=row):
						horizontal_roads_under_construction.append(node[row][colm]+'-'+node[row][colm+1])
					res = colm;resw=row
	horizontal_roads_under_construction.sort()
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
	image = cv2.rotate(maze_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
	res = 10
	row = 0
	colm = 0
	i = 0
	j = 0
	resw=10
	nodes =[['F1','F2','F3','F4','F5','F6'],
			['E1','E2','E3','E4','E5','E6'],
			['D1','D2','D3','D4','D5','D6'],
			['C1','C2','C3','C4','C5','C6'],
			['B1','B2','B3','B4','B5','B6'],
		    ['A1','A2','A3','A4','A5','A6']]
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (3,3), 0)
	thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
	horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
	horizontal_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
	horizontal_mask = cv2.dilate(horizontal_mask, horizontal_kernel, iterations=19)
	result = horizontal_mask-thresh
	result = result[0:606, 106:594]
	result = cv2.resize(result,(50,60))
	for i in range(1,60):
		for j in range(1,50):
			if (result[i][j]==255):
				row =int(i/10);colm=int(j/10)
				if(colm!=res or resw!=row):
					vertical_roads_under_construction.append(nodes[row][colm]+'-'+nodes[row][colm+1])
				res = colm;resw=row


	vertical_roads_under_construction.sort()
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
	def colour(B,G,R):
		skyblue = [255,255,0]
		green = [0,255,0]
		pink = [180,0,255]
		orange = [0,127,255]
		if(B==skyblue[0] and G==skyblue[1] and R==skyblue[2]):   
			return 'Skyblue'
		elif(B==pink[0] and G==pink[1] and R==pink[2]):
			return 'Pink'
		elif(B==green[0] and G==green[1] and R==green[2]):
			return 'Green'
		elif(B==orange[0] and G==orange[1] and R==orange[2]):
			return 'Orange'
	def List(a,b,c,d,e):
		shop_contour=[]
		shop_contour.append(a)
		shop_contour.append(b)
		shop_contour.append(c)
		shop_contour.append([d,e])
		medicine_packages.append(shop_contour)

	img = maze_image
	imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
	contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	for contour in contours:
		approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
		cv2.drawContours(img, [approx], 0, (0, 0, 0), 1)
		x = approx.ravel()[0]
		y = approx.ravel()[1] - 5
		if len(approx) == 4:
			if(109<x<187 and 105<y<194):
				a='Shop_1'
				B,G,R=img[y+10][x+10]
				b=colour(B,G,R)
				c='Square'
				d=x+10
				e=y+15
				List(a,b,c,d,e)
			elif(209<x<287 and 105<y<194):
				a='Shop_2'
				B,G,R=img[y+10][x+10]
				b=colour(B,G,R)
				c='Square'
				d=x+10
				e=y+15
				List(a,b,c,d,e)
			elif(309<x<390 and 105<y<194):
				a='Shop_3'
				B,G,R=img[y+10][x+10]
				b=colour(B,G,R)
				c='Square'
				d=x+10
				e=y+15
				List(a,b,c,d,e)
			elif(409<x<490 and 105<y<194):
				a='Shop_4'
				B,G,R=img[y+10][x+10]
				b=colour(B,G,R)
				c='Square'
				d=x+10
				e=y+15
				List(a,b,c,d,e)
			elif(509<x<590 and 105<y<194):
				a='Shop_5'
				B,G,R=img[y+10][x+10]
				b=colour(B,G,R)
				c='Square'
				d=x+10
				e=y+15
				List(a,b,c,d,e)
			elif(609<x<610 and 105<y<194):
				a='Shop_6'
				B,G,R=img[y+10][x+10]
				b=colour(B,G,R)
				c='Square'
				d=x+10
				e=y+15
				List(a,b,c,d,e)

		elif len(approx) == 3 :
			if(105<x<194 and 105<y<194):
				a='Shop_1'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Triangle'
				d=x
				e=y+18
				List(a,b,c,d,e)
			elif(209<x<287 and 105<y<194):
				a='Shop_2'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Triangle'
				d=x
				e=y+18
				List(a,b,c,d,e)
			elif(309<x<390 and 105<y<194):
				a='Shop_3'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Triangle'
				d=x
				e=y+18
				List(a,b,c,d,e)
			elif(409<x<490 and 105<y<194):
				a='Shop_4'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Triangle'
				d=x
				e=y+18
				List(a,b,c,d,e)
			elif(509<x<590 and 105<y<194):
				a='Shop_5'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Triangle'
				d=x
				e=y+18
				List(a,b,c,d,e)
			elif(609<x<610 and 105<y<194):
				a='Shop_6'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Triangle'
				d=x
				e=y+18
				List(a,b,c,d,e)
		else:

			if(105<x<194 and 105<y<194):
				a='Shop_1'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Circle'
				d=x
				e=y+17
				List(a,b,c,d,e)

			elif(209<x<287 and 105<y<194):
				a='Shop_2'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Circle'
				d=x
				e=y+17
				List(a,b,c,d,e)
			elif(309<x<390 and 105<y<194):
				a='Shop_3'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Circle'
				d=x
				e=y+17
				List(a,b,c,d,e)
			elif(409<x<490 and 105<y<194):
				a='Shop_4'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Circle'
				d=x
				e=y+17
				List(a,b,c,d,e)
			elif(509<x<590 and 105<y<194):
				a='Shop_5'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Circle'
				d=x
				e=y+17
				List(a,b,c,d,e)
			elif(609<x<690 and 105<y<194):
				a='Shop_6'
				B,G,R=img[y+10][x]
				b=colour(B,G,R)
				c='Circle'
				d=x
				e=y+17
				List(a,b,c,d,e)
	medicine_packages.sort()

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
	traffic_signals,start_node,end_node = detect_traffic_signals(maze_image)
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	medicine_packages = detect_medicine_packages(maze_image)
	arena_parameters['traffic_signals']=traffic_signals
	arena_parameters['start_node']=start_node
	arena_parameters['end_node']=end_node
	arena_parameters['horizontal_roads_under_construction']= horizontal_roads_under_construction
	arena_parameters['vertical_roads_under_construction'] = vertical_roads_under_construction
	arena_parameters['medicine_packages']=medicine_packages
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path ="C:\\Users\\HARI\\Downloads\\PB_Task1_Windows\\PB_Task1_Windows\\Task1A\\public_test_images\\"

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