'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1B of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		connect_to_server, send_to_receive_from_server, find_new_path
# 					[ Comma separated list of functions in this file ]
# Global variables:	SERVER_IP, SERVER_PORT, SERVER_ADDRESS
# 					[ List of global variables defined in this file ]


# Import necessary modules
# Do not import any other modules
import cv2
import socket
import sys
import os
from datetime import datetime

# IP address of server (for now, loopback address)
SERVER_IP = '127.0.0.1'

# Port number assigned to server
SERVER_PORT = 3333
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)


def connect_to_server(SERVER_ADDRESS):

	"""
	Purpose:
	---
	the function creates socket connection with server

	Input Arguments:
	---
	`SERVER_ADDRESS` :	[ tuple ]
		port address of server

	Returns:
	---
	`sock` :	[ object of socket class ]
		object of socket class for socket communication

	Example call:
	---
	sock = connect_to_server(SERVER_ADDRESS)

	"""

	sock = None
	
	#############  Add your Code here   ###############

	sock=socket.socket()
	sock.connect(SERVER_ADDRESS)

	###################################################

	return sock


def send_to_receive_from_server(sock, shortestPath):

	"""
	Purpose:
	---
	the function sends / receives data to / from server

	Input Arguments:
	---
	`sock` :	[ object of socket class ]
		object of socket class for socket communication
	`shortestPath`	:	[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Returns:
	---
	`sent_data` :	[ string ]
		data sent from client to server in proper format
	`recv_data` :	[ string ]
		data sent from server to client in proper format

	Example call:
	---
	sent_data, recv_data = send_to_receive_from_server(sock, shortestPath)

	"""
	s = str(shortestPath)
	shortestPathString = "#"+s+"#"
	sent_data = ''
	recv_data = ''

	#############  Add your Code here   ###############
	sent_data=sock.send(shortestPathString)
	recv_data=sock.recv(1024)
	###################################################

	return sent_data, recv_data

##  Function that computes new shortest path from cell adjacent to obstacle to final_point
def find_new_path(recv_data, shortestPath):

	"""
	Purpose:
	---
	the function computes new shortest path from cell adjacent to obstacle to final_point

	Input Arguments:
	---
	`recv_data` :	[ string ]
		data sent from server to client in proper format
	`shortestPath`	:	[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Returns:
	---
	`obstacle_coord` :	[ tuple ]
		position of dynamic obstacle in (x,y) coordinate
	`new_shortestPath` :	[ list ]
		list of coordinates of shortest path from new_initial_point to final_point
	`new_initial_point` :	[ tuple ]
		coordinate of cell adjacent to obstacle for the new shortest path
	`img` :	[ numpy array ]

	Example call:
	---
	obstacle_coord, new_shortestPath, new_initial_point, img = find_new_path(recv_data, shortestPath)

	"""

	global obstacle_coord 
	obstacle_coord = ()
	new_shortestPath = []
	new_initial_point = ()

	global img_file_path, final_point, no_cells_height, no_cells_width

	#############  Add your Code here   ###############
	o = list(recv_data)
	o.remove('@')
	o.remove('@')
	o.remove('(')
	o.remove(')')
	s = "".join(o)
	result = [x.strip() for x in s.split(',')]
	obstacle_coord = tuple(list(map(int,result)))

	x = shortestPath.index(obstacle_coord)
	new_initial_point  = shortestPath[x-1]
	new_shortestPath = shortestPath(readImage(img_file_path),new_initial_point,(9,9),20,20,obstacle_coord)

	###################################################

	return obstacle_coord, new_shortestPath, new_initial_point, img


#############	You can add other helper functions here		#############
# Maze images in task_1a_images folder have cell size of 20 pixels
CELL_SIZE = 20



class Link():
    value = 0
    parent = 0
    def __init__(self, a, b):
        self.value = a
        self.parent = b


## The findNeighbours function takes a maze image and row and column coordinates of a cell as input arguments
## and returns a stack consisting of all the neighbours of the cell as output.
## Note :- Neighbour refers to all the adjacent cells one can traverse to from that cell provided only horizontal
## and vertical traversal is allowed.
## You can copy the code you wrote for section1.py here.
def findNeighbours(img,row,column):
    neighbours = []
    #############  Add your Code here   ###############
    i = 0
    while(True):
        if img[i, i] != 0:
            border = i 
            break
        i += 1
    i = border
    cell = 0
    while(True):
        if img[i, i] == 0:
            cell = i 
            break
        i += 1
    if img[cell - border * 2, cell] == 0 or img[cell, cell - border * 2] == 0:
        cell = cell + border
    row_new = int((2 * row + 1) * (cell / 2))
    col_new = int((2 * column + 1) * (cell / 2))
    top = int(row_new - (cell / 2) + 1)
    bottom = int(row_new + (cell / 2) - 2)
    left = int(col_new - (cell / 2) + 1)
    right = int(col_new + (cell / 2) - 2)
    if img[top, col_new] != 0:
        neighbours.append([row - 1, column])
    if img[bottom, col_new] != 0:
        neighbours.append([row + 1, column])
    if img[row_new, left] != 0:
        neighbours.append([row, column - 1])
    if img[row_new, right] != 0:
        neighbours.append([row, column + 1])
    ###################################################
    return neighbours



##  returns the graph of the maze image
def build_graph(img):  
    graph = {}
    #############  Add your Code here   ###############
    i = 0
    while(True):
        if img[i, i] != 0:
            border = i 
            break
        i += 1
    i = border
    cell = 0
    while(True):
        if img[i, i] == 0:
            cell = i 
            break
        i += 1
    if img[cell - border * 2, cell] == 0 or img[cell, cell - border * 2] == 0:
        cell = cell + border
    r = len(img) // cell
    c = len(img) // cell
    for i in range(r):
        for j in range(c):
            graph[(i, j)] = findNeighbours(img, i, j)
    ###################################################

    return graph

def next_num():          #assigning numbers to the cells 
    del x[0]
    return x[0]

def numberMaze(graph, initial, new, l):         
    c = 0                                                                      
    
    for k in graph[initial]:
        if new[tuple(k)] == -1:
            c += 1
    if c == 0:
        return
    elif c == 1:
        for i in range(len(graph[initial])):        
            if new[tuple(graph[initial][i])] == -1:
                new[tuple(graph[initial][i])] = new[initial] 
                numberMaze(graph, tuple(graph[initial][i]), new, l) 
    else:
        for i in range(len(graph[initial])):
            if new[tuple(graph[initial][i])] == -1:
                n = next_num()
                new[tuple(graph[initial][i])] = n
                l.append(Link(n, new[initial]))
                numberMaze(graph, tuple(graph[initial][i]), new, l)

def shortest_path(l, initial, final, path):      ##finds the shortest path
                                                         
    if final == initial:
        return
    else:
        for i in l:
            if i.value == final:
                parent = i.parent
                break
        path.append(parent)
        shortest_path(l, initial, parent, path)
    parent = 0
    




def readImage(img_file_path):

	"""
	Purpose:
	---
	the function takes file path of original image as argument and returns it's binary form
	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image
	Returns:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path
	Example call:
	---
	original_binary_img = readImage(img_file_path)
	"""
	


	#############	Add your Code here	###############
	
	mazeImg = cv2.imread(img_file_path,0)
	ret,binary_img = cv2.threshold(mazeImg,10,255,cv2.THRESH_BINARY)
	
	###################################################

	return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width, obs):
	
	"""
	Purpose:
	---
	the function takes binary form of original image, start and end point coordinates and solves the maze
	to return the list of coordinates of shortest path from initial_point to final_point
	Input Arguments:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path
	`initial_point` :		[ tuple ]
		start point coordinates
	`final_point` :			[ tuple ]
		end point coordinates
	`no_cells_height` :		[ int ]
		number of cells in height of maze image
	`no_cells_width` :		[ int ]
		number of cells in width of maze image
	Returns:
	---
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point
	Example call:
	---
	shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)
	"""
	
	
	global shortestPath
	shortestPath = []

	#############	Add your Code here	###############

	shortest = [initial_point]
	visited = [initial_point]
	visited.append(obs)
	count = 1
	
	
	global new
	new = {}
	global l
	l = []
	breadth = len(original_binary_img)/20          
	length = len(original_binary_img[0])/20          
	if length == 10:
		#initial_point = (0,0)      
		final_point = (9,9)           
	else:
		#initial_point = (0,0)
		final_point = (19,19)
	graph = build_graph(original_binary_img)
	for k in graph.keys():
		new[k] = -1
		new[initial_point] = 1
	global x
	x = list(range(1, 1000))
	numberMaze(graph, initial_point, new, l)
	shortestPath.append(new[final_point])
	shortest_path(l, new[initial_point], new[final_point], shortestPath)
	shortestPath.reverse()
	current = initial_point
	while(True):
		if (current == final_point):
			return shortest
		for j in graph[current]:
			if not tuple(j) in visited:
				if new[tuple(j)] == new[current]:
					current = tuple(j)
					shortest.append(current)
					visited.append(current)
					break
				else:
					if new[tuple(j)] == shortestPath[count]:
						count += 1
						shortest.append(tuple(j))
						current = tuple(j)
						visited.append(current)
						break

	###################################################
	
	return shortestPath


#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling connect_to_server,
# 					find_new_path and send_to_receive_from_server functions, it then asks the user whether to repeat
# 					the same on all maze images	present in 'task_1b_images' folder or not

if __name__ == '__main__':
	
	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1b_images/'				# path to directory of 'task_1c_images'

	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	# Importing task_1a and image_enhancer script
	try:
		task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
		sys.path.append(task_1a_dir_path)

		import task_1a
		import image_enhancer

	except Exception as e:
		print('\n[ERROR] task_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
		exit()
	
	# To log data received from server
	output_file_name = 'data_from_server.txt'

	# remove the previously generated output txt file if exists
	if os.path.exists(output_file_name):
		os.remove(output_file_name)
	
	try:
	
		print('\n============================================')
		print('\nFor maze0' + str(file_num) + '.jpg')
		
		# Create socket connection with server
		try:
			sock = connect_to_server(SERVER_ADDRESS)

			if sock == None:
				print('\n[ERROR] connect_to_server function is not returning socket object in expected format !\n')
				exit()
			
			else:
				print('\nConnecting to %s Port %s' %(SERVER_ADDRESS))
		
		except ConnectionRefusedError as connect_err:
			print('\n[ERROR] the robot-server.c file is not executing, start the server first !\n')
			exit()
		
		try:		
			original_binary_img = task_1a.readImage(img_file_path)
			height, width = original_binary_img.shape

		except AttributeError as attr_err:
			print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
			exit()
		
		no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
		no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
		initial_point = (0, 0)											# start point coordinates of maze
		final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

		try:
			shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

			if len(shortestPath) > 2:
				img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
				
			else:
				print('\n[ERROR] shortestPath returned by solveMaze function in task_1a.py is incomplete !\n')
				exit()
		
		except TypeError as type_err:
			print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
			exit()

		print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

		cv2.imshow('canvas0' + str(file_num) + '_original_path', img)
		cv2.waitKey(0)

		sent_data, recv_data = send_to_receive_from_server(sock, shortestPath)

		if (sent_data.count('#') == 2) and (recv_data.count('@') == 2):
			print('\nSending %d bytes of data to server = %s' %(len(sent_data), sent_data))
			print('\nReceived %d bytes of data from server = %s' %(len(recv_data), recv_data))

			output_file = open(output_file_name, 'w')
			output_file.write('maze0' + str(file_num) + '.jpg' + '\n')
			output_file.write(recv_data[:-1] + '\n')

		else:
			print('\n[ERROR] sent / received data to / from server is not in proper format !\n')
			exit()

		obstacle_count = 0
		obstacle_list = []
		obstacle_pos = 0

		while '$' not in recv_data:

			obstacle_count = obstacle_count + 1

			try:
				obstacle_coord, new_shortestPath, new_initial_point, img = find_new_path(recv_data, shortestPath)

				if len(new_shortestPath) > 2:
					img = image_enhancer.highlightPath(img, new_initial_point, final_point, new_shortestPath)
					
					print('\nDynamic Obstacle found at = (%d,%d)' %(obstacle_coord[0], obstacle_coord[1]))
					print('\n--------------------------------------------')
					print('\nNew Shortest Path = %s \n\nLength of new Path = %d' % (new_shortestPath, len(new_shortestPath)))
				
				else:
					print('\n[ERROR] shortestPath returned by solveMaze function in task_1a.py is incomplete !\n')
					exit()
			
			except TypeError as type_err:
				print('\n[ERROR] find_new_path function is not returning new shortest path in maze image in expected format !\n')
				exit()

			except IndexError as idx_err:
				print('\n[ERROR] find_new_path function is not returning obstacle coordinates in expected format !\n')
				exit()

			cv2.imshow('canvas0' + str(file_num) + '_obstacle_' + str(obstacle_count), img)
			cv2.waitKey(0)

			shortestPath = new_shortestPath
			sent_data, recv_data = send_to_receive_from_server(sock, shortestPath)

			if (sent_data.count('#') == 2) and (recv_data.count('@') == 2):
				print('\nSending %d bytes of data to server = %s' %(len(sent_data), sent_data))
				print('\nReceived %d bytes of data from server = %s' %(len(recv_data), recv_data))
				output_file.write(recv_data[:-1] + '\n')

			else:
				print('\n[ERROR] sent / received data to / from server is not in proper format !\n')
				exit()
		
		if (obstacle_count == 0):	print('\nNo Dynamic Obstacle for the image')
		
		else:	print('\nNo more Dynamic Obstacle for the image')

		print('\n============================================')
		
		cv2.imshow('canvas0' + str(file_num) + '_final_path', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
		output_file.write(current_time + '\n')
		
		output_file.close()

		choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

		if choice == 'y':

			if os.path.exists(output_file_name):

				os.remove(output_file_name)
			
			output_file = open(output_file_name, 'w')

			file_count = len(os.listdir(img_dir_path))

			for file_num in range(file_count):

				img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

				print('\n============================================')
				print('\nFor maze0' + str(file_num) + '.jpg')
				
				try:		
					original_binary_img = task_1a.readImage(img_file_path)
					height, width = original_binary_img.shape

				except AttributeError as attr_err:
					print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
					exit()
				
				no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
				no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
				initial_point = (0, 0)											# start point coordinates of maze
				final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

				try:
					shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

					if len(shortestPath) > 2:
						img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
						
					else:
						print('\n[ERROR] shortestPath returned by solveMaze function in task_1a.py is incomplete !\n')
						exit()
				
				except TypeError as type_err:
					print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
					exit()

				print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

				cv2.imshow('canvas0' + str(file_num) + '_original_path', img)
				cv2.waitKey(0)

				sent_data, recv_data = send_to_receive_from_server(sock, shortestPath)

				if (sent_data.count('#') == 2) and (recv_data.count('@') == 2):
					print('\nSending %d bytes of data to server = %s' %(len(sent_data), sent_data))
					print('\nReceived %d bytes of data from server = %s' %(len(recv_data), recv_data))

					# output_file = open(output_file_name, 'w')
					output_file.write('maze0' + str(file_num) + '.jpg' + '\n')
					output_file.write(recv_data[:-1] + '\n')

				else:
					print('\n[ERROR] sent / received data to / from server is not in proper format !\n')
					exit()

				obstacle_count = 0
				obstacle_list = []
				obstacle_pos = 0

				while '$' not in recv_data:

					obstacle_count = obstacle_count + 1

					try:
						obstacle_coord, new_shortestPath, new_initial_point, img = find_new_path(recv_data, shortestPath)

						if len(new_shortestPath) > 2:
							img = image_enhancer.highlightPath(img, new_initial_point, final_point, new_shortestPath)
							
							print('\nDynamic Obstacle found at = (%d,%d)' %(obstacle_coord[0], obstacle_coord[1]))
							print('\n--------------------------------------------')
							print('\nNew Shortest Path = %s \n\nLength of new Path = %d' % (new_shortestPath, len(new_shortestPath)))
						
						else:
							print('\n[ERROR] shortestPath returned by solveMaze function in task_1a.py is incomplete !\n')
							exit()
					
					except TypeError as type_err:
						print('\n[ERROR] find_new_path function is not returning new shortest path in maze image in expected format !\n')
						exit()

					except IndexError as idx_err:
						print('\n[ERROR] find_new_path function is not returning obstacle coordinates in expected format !\n')
						exit()
					
					except Exception as e:
						raise e

					cv2.imshow('canvas0' + str(file_num) + '_obstacle_' + str(obstacle_count), img)
					cv2.waitKey(0)

					shortestPath = new_shortestPath
					sent_data, recv_data = send_to_receive_from_server(sock, shortestPath)

					if (sent_data.count('#') == 2) and (recv_data.count('@') == 2):
						print('\nSending %d bytes of data to server = %s' %(len(sent_data), sent_data))
						print('\nReceived %d bytes of data from server = %s' %(len(recv_data), recv_data))
						output_file.write(recv_data[:-1] + '\n')

					else:
						print('\n[ERROR] sent / received data to / from server is not in proper format !\n')
						exit()
				
				if (obstacle_count == 0):	print('\nNo Dynamic Obstacle for the image')
				
				else:	print('\nNo more Dynamic Obstacle for the image')

				print('\n============================================')
				
				cv2.imshow('canvas0' + str(file_num) + '_final_path', img)
				cv2.waitKey(0)
				cv2.destroyAllWindows()

			current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
			output_file.write(current_time + '\n')
			
			output_file.close()

			print('\nClosing Socket')
			sock.close()
		
		else:
			
			print('\nClosing Socket')
			sock.close()
	
	except KeyboardInterrupt:
		print('\nClosing Socket')
		sock.close()

