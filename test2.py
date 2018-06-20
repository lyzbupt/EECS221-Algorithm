'''					
fileName = "/Users/liyuanzhe/Documents/EECS221Alogrithm/week7/warehouseOutput.txt"
i=1
orderNumber =2
with open( fileName, 'rb') as f:
	lines = f.readlines()
	for line in lines:
							
		if(i == orderNumber):

			#line = line.split(',')
			c = eval(line)

			print "c[0],c[1],c[2],c[3] is", c[0],c[1],c[2],c[3]
			print type(list(c[1]))
			print type(c[2])
			print "For order ", i, " \n"

			
			#print logStr
			#print "line[0]", line[1]
		i = i+1

num = [11, 22, 33]
k = num.pop(0)
s = []
s.append(k)
print s
print num
'''


import os
import csv
import re
import time

import copy
import heapq 
import sys
from path import getPath
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


def find_item( grid, item_Cor, car):
	route = []
	#print 'Item coordination in grid is: ' + str(item_Cor)
	#print ''
	#print car
	if(item_Cor[0]>car[0]):    # WEST

		dist = [item_Cor[0]-1, item_Cor[1]] # Left pick	
		#print '11'	
		if(item_Cor[1]>car[1]): # south WEST
			#print '2'
			if (car[1]%2 != 0):  # odd, to east
				#print '3'
				for i in range(car[0], dist[0]): # odd, to east
					route.append([i,car[1]])
				for i in range(car[1], dist[1]): # odd, to north
					route.append([dist[0],i])
			else:
				for i in range(car[1], dist[1]):	# even, to north
					route.append([car[0],i])
				for i in range(car[0]+1, item_Cor[0]):	# even, to east
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
				for i in range(car[0]+1, item_Cor[0]):	# even, to east
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
				for i in range(1, car[0]- item_Cor[0]):	# even, to east
					route.append([car[0]-i,dist[1]+1])
			route.append(dist)

	return route, dist

def gePath( grid, begin, destination,order):			# generate path
	print order
	carPosition = begin
	path=[]
	for item in order:
		path1, carPosition = find_item(grid, item_position(grid,item), carPosition)
		path.append(path1)
	path1, carPosition = find_item(grid, destination, carPosition)
	path.append(path1)
	return path

grid = build_grid()
itemsID = [46071, 379019,70172,1321,2620261]
path = getPath(grid, [1,1], [20,20],itemsID)
s = "ww"+str([1,1,1])
print path
