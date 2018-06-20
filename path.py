#EECS 221 Adv App Algorithms
#Project name: Project week10
#Author: Yuanzhe Li
#Student ID: 14563990
#Date: June/10/2018
#Language: Python 2.7
#Algorithm
import os
import csv
import re
import time
import copy
import heapq 
import sys

def item_position( grid, itemID):    # return item positon in coordination
	return grid[itemID]


def build_grid():
	grid = {}
	if False == os.path.isfile('warehouse-grid.csv'):
		print "warehouse-grid.csv is not exist."
		return 0
	with open( 'warehouse-grid.csv', 'rb') as f:
		data = csv.reader(f)
		for row in data:

			grid[int(row[0])] = [int(float(row[1]))*2, int (row[2])*2]

	f.close()
	return grid


def find_item( grid, item_Cor, car):    #[19,19]- [5,18] ;-- [19,19]
	route = []
	#print 'Item coordination in grid is: ' + str(item_Cor)
	#print ''
	#print car
	'''
	if (item_Cor[0]%2!=0 and item_Cor[1]%2!=0):  # odd destination
		dist = item_Cor



		return route, dist
	'''
	if(item_Cor[0]>car[0]):    # WEST

		dist = [item_Cor[0]-1, item_Cor[1]] # Left pick	
		if(item_Cor[1]>car[1]): # south WEST
			if (car[1]%2 != 0):  # odd, to east
				for i in range(car[0], dist[0]): # odd, to east
					route.append([i,car[1]])
				for i in range(car[1], dist[1]): # odd, to north
					route.append([dist[0],i])
			else:# even
				for i in range(car[1], dist[1]):	# even, to north
					route.append([car[0],i])
				for i in range(car[0], item_Cor[0]):	# even, to east
					route.append([i,item_Cor[1]-1])
			route.append(dist)
		else:				# north WEST
			if (car[1]%2 != 0):  # odd, to east
				for i in range(car[0], dist[0]): # odd, to east
					route.append([i,car[1]])
				for i in range(car[1] - dist[1]): # odd, to south
					route.append([dist[0],car[1]-i])
			else:
				for i in range(car[1] - dist[1]):	# even, to south
					route.append([car[0],car[1]-i])
				for i in range(car[0], item_Cor[0]):	# even, to east
					route.append([i,item_Cor[1]+1])
			route.append(dist)


	else:						# EAST
		dist = [item_Cor[0]+1, item_Cor[1]] # right pick
		if(item_Cor[1]>car[1]): # south EAST
			if (car[1]%2 != 0):  # odd, to west
				for i in range(car[0]-dist[0]): # odd, to west
					route.append([car[0]-i,car[1]])
				for i in range(car[1], dist[1]): # odd, to north
					route.append([dist[0],i])
			else:
				for i in range(car[1], dist[1]):	# even, to north
					route.append([car[0],i])
				for i in range(1, car[0]- item_Cor[0]):	# even, to west
					route.append([car[0]-i,dist[1]-1])
			route.append(dist)
		else:				# north EAST
			if (car[1]%2 != 0):  # odd, to east
				for i in range(car[0] - dist[0]): # odd, to east
					route.append([car[0]-i,car[1]])
				for i in range(car[1] - dist[1]): # odd, to south
					route.append([dist[0],car[1]-i])
			else:
				for i in range(car[1] - dist[1]):	# even, to south
					route.append([car[0],car[1]-i])
				for i in range(0, car[0]- item_Cor[0]):	# even, to east
					route.append([car[0]-i,dist[1]+1])
			route.append(dist)

	return route, dist

def find_item_des( grid, destination, car):    #[19,19]- [5,18] ;-- [19,19]
	route = []
	dist = destination
	if (destination[1]>car[1]):
		if(destination[0]>car[0]):
			for i in range(car[1],destination[1]):
				route.append([car[0],i])
			for i in range(car[0],destination[0]):
				route.append([i,destination[1]])
		else:
			for i in range(car[1],destination[1]):
				route.append([car[0],i])
			for i in range(car[0]-destination[0]):
				route.append([car[0]-i,destination[1]])
	else:
		if(destination[0]>car[0]):
			for i in range(car[1]-destination[1]):
				route.append([car[0],car[1]-i])
			for i in range(car[1],destination[1]):
				route.append([i,destination[1]])
		else:
			for i in range(car[1]-destination[1]):
				route.append([car[0],car[1]-i])
			for i in range(car[0]-destination[0]):
				route.append([car[0]-i,destination[1]])

	route.append(destination)
	return route, dist


def getPath( grid, begin, destination,order):			# generate path
	print order
	carPosition = begin
	path=[]
	for item in order:
		path1, carPosition = find_item(grid, item_position(grid,item), carPosition)
		path.append(path1)
	path1, carPosition = find_item_des(grid, destination, carPosition)
	path.append(path1)
	return path
'''
grid = build_grid()
itemsID = [46071, 379019,70172,1321,2620261]
path = getPath(grid, [1,1], [21,21],itemsID)

print path
'''