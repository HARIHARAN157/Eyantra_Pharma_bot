'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ PB_4232]
# Author List:		[ HARIHARAN S, PARTHIBAN V, AJAY PRANAV P R, MAVEENKUMAR S ]
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def remove(paths,maze_image):
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
						del paths[node[row][colm]][node[row][colm+1]]
						del paths[node[row][colm+1]][node[row][colm]]
					res = colm;resw=row
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
					del paths[nodes[row][colm]][nodes[row][colm+1]]
					del paths[nodes[row][colm+1]][nodes[row][colm]]
				res = colm;resw=row
	return paths
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

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

	##############	ADD YOUR CODE HERE	##############
	maze_image = image
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
	##################################################

	return traffic_signals, start_node, end_node


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node
			Eg. : { "D3":{"C3", "E3", "D2", "D4" }, 
					"D5":{"C5", "D2", "D6" }  }
	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    

	paths = {}
	##############	ADD YOUR CODE HERE	##############
	adjacent_node = {}
	indented_node = {}
	nodes =[['A1','B1','C1','D1','E1','F1'],
	        ['A2','B2','C2','D2','E2','F2'],
			['A3','B3','C3','D3','E3','F3'],
			['A4','B4','C4','D4','E4','F4'],
			['A5','B5','C5','D5','E5','F5'],
			['A6','B6','C6','D6','E6','F6']]
	for i in range(0,6):
		for j in range(0,6):
			a = i+1;b = i-1;c = j+1;d = j-1
			if(d<0 and b<0):
				adjacent_node[nodes[i][j+1]] = 1
				adjacent_node[nodes[i+1][j]] = 1
			elif(b<0 and c==6):
				adjacent_node[nodes[i][j-1]] = 1
				adjacent_node[nodes[i+1][j]] = 1
			elif(a==6 and c==6):
				adjacent_node[nodes[i][j-1]] = 1
				adjacent_node[nodes[i-1][j]] = 1
			elif(a==6 and d<0):
				adjacent_node[nodes[i][j+1]] = 1
				adjacent_node[nodes[i-1][j]] = 1
			elif(a==6):
				adjacent_node[nodes[i][j-1]] = 1
				adjacent_node[nodes[i][j+1]] = 1
				adjacent_node[nodes[i-1][j]] = 1
			elif(b<0):
				adjacent_node[nodes[i][j-1]] = 1
				adjacent_node[nodes[i][j+1]] = 1
				adjacent_node[nodes[i+1][j]] = 1
			elif(c==6):
				adjacent_node[nodes[i][j-1]] = 1
				adjacent_node[nodes[i-1][j]] = 1
				adjacent_node[nodes[i+1][j]] = 1
			elif(d<0):
				adjacent_node[nodes[i][j+1]] = 1
				adjacent_node[nodes[i-1][j]] = 1
				adjacent_node[nodes[i+1][j]] = 1
			else:
				adjacent_node[nodes[i][j-1]] = 1
				adjacent_node[nodes[i][j+1]] = 1
				adjacent_node[nodes[i-1][j]] = 1
				adjacent_node[nodes[i+1][j]] = 1
			indented_node=adjacent_node.copy()
			paths[nodes[i][j]] = indented_node
			adjacent_node.clear()
	paths = remove(paths,image)
	##################################################

	return paths



def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

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

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}
	##############	ADD YOUR CODE HERE	##############
	traffic_signals, start_node, end_node=detect_all_nodes(maze_image)
	paths=detect_paths_to_graph(maze_image)
	arena_parameters["traffic_signals"]=traffic_signals
	arena_parameters["start_node"]=start_node
	arena_parameters["end_node"]=end_node
	arena_parameters["paths"]=paths
	##################################################
	
	return arena_parameters

def path_planning(graph, start, end):

		"""
		Purpose:
		---
		This function takes the graph(dict), start and end node for planning the shortest path

		** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
		list given below **

		Input Arguments:
		---
		`graph` :	[ numpy array ]
				numpy array of image returned by cv2 library
		`start` :	str
				name of start node
		`end` :		str
				name of end node


		Returns:
		---
		`backtrace_path` : [ list of nodes ]
				list of nodes, produced using path planning algorithm

			eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
		
		Example call:
		---
		arena_parameters = detect_arena_parameters(maze_image)
		"""
		backtrace_path=[]
		##############	ADD YOUR CODE HERE	##############
		def find_shortest_path(graph, start, end, path=[]):
					path = path + [start]
					if start == end:
						return path
					shortest = None
					for node in graph[start]:
						if node not in path:
							newpath = find_shortest_path(graph, node, end, path)
							if newpath:
								if not shortest or len(newpath) < len(shortest):
									shortest = newpath
					return shortest
		backtrace_path=find_shortest_path(graph, start, end, path=[])
		##################################################
		
		return backtrace_path

def paths_to_moves(paths, traffic_signal):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]
	##############	ADD YOUR CODE HERE	##############
	def index(var):
		for i in range(0,6):
			for j in range(0,6):
				if nodes[i][j]==var:
					return [i,j]
	nodes =[['A1','B1','C1','D1','E1','F1'],
	        ['A2','B2','C2','D2','E2','F2'],
			['A3','B3','C3','D3','E3','F3'],
			['A4','B4','C4','D4','E4','F4'],
			['A5','B5','C5','D5','E5','F5'],
			['A6','B6','C6','D6','E6','F6']]
	moves=[]
	a=1;b=0;c=0
	R="RIGHT"
	L="LEFT"
	RE="REVERSE"
	def swap(a,b,d,c):
		if (c==0):
			moves.append(d)
		elif(c==1):
			if(d==L):
				moves.append(R)
			elif(d==R):
				moves.append(L)
		return b,a
	List=[]
	for i in range(0,len(paths)):
		ind=index(paths[i])
		List.append(ind)
	for i in range(0,len(List)-1):
		if(paths[i] in traffic_signal):
				moves.append("WAIT_5")
		if(a==1):
				if(List[i][1]==List[i+1][1]):
					moves.append("STRAIGHT")
				elif(List[i][1]<List[i+1][1]):
					a,b=swap(a,b,R,c)
					c=1
				elif(List[i][1]>List[i+1][1]):
					c=0
					a,b=swap(a,b,L,c)
		else:
				if(List[i][0]==List[i+1][0]):
					moves.append("STRAIGHT")
				elif(List[i][0]<List[i+1][0]):
					a,b=swap(a,b,L,c)
					c=0
				elif(List[i][0]>List[i+1][0]):
					a,b=swap(a,b,R,c)
					c=0
	list_moves=moves
	##################################################
	return list_moves

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "test_images/"

	for file_num in range(0,10):
			
			img_key = 'maze_00' + str(file_num)
			img_file_path = "C:\\Users\\HARI\\Downloads\\PB_Task3A_Windows\\PB_Task3A_Windows\\test_images\\" + img_key  + '.png'
			# read image using opencv
			image = cv2.imread(img_file_path)
			
			# detect the arena parameters from the image
			arena_parameters = detect_arena_parameters(image)
			print('\n============================================')
			print("IMAGE: ", file_num)
			print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )

			# path planning and getting the moves
			back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
			moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

			print("PATH PLANNED: ", back_path)
			print("MOVES TO TAKE: ", moves)

			# display the test image
			cv2.imshow("image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()