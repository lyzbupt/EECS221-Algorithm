#EECS 221 Adv App Algorithms
#Project name: Project week7
#Author: Yuanzhe Li
#Student ID: 14563990
#Date: May/20/2018
#Language: Python 2.7
# nearest neighbor Algorithm
import os
import csv
import re
import time
#from guppy import hpy
import copy
import heapq 
import sys

class NN():

	def __init__(self, grid, item_dimTab):
		self.grid = grid
		self.item_dimTab = item_dimTab
		self.beginning = []
		self.destination = []
		self.itemsID = []
		self.W = True

	def find_item(self, item_Cor, car):
		grid = self.grid
		item_dimTab = self.item_dimTab 
		route = []
		if(item_Cor[0]>car[0]):    # WEST
			dist = [item_Cor[0]-1, item_Cor[1]] # Left pick	
			if(item_Cor[1]>car[1]): # south WEST
				if (car[1]%2 != 0):  # odd, to east
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

	def item_position(self, itemID):    # return item positon in coordination
		grid = self.grid
		return grid[itemID]

	def distance(self, posN1, posN2):			# return distance between two positions
		return (abs(posN1[0]-posN2[0])+abs(posN1[1]-posN2[1]))

	def gePath(self, begin, destination,order):			# generate path
		grid = self.grid
		carPosition = begin
		path=[]
		for item in order:
			path1, carPosition = self.find_item(self.item_position(grid,item), carPosition)
			path.append(path1)
		path1, carPosition = self.find_item(destination, carPosition)
		path.append(path1)
		return path

	def pathDist(self, path):
		num = 0
		for path0 in path:
			#print type(path0), path0
			num = num + len(path0)
		return num

	def displayPath(self, optimalOrder, path, beginning, destination, num):   # final fucntion, to display
		#beginning = self.beginning
		#destination = self.destination
		#itemsID = self.itemsID
		print "Here is the optimal picking order:" 
		print optimalOrder
		print "\nHere is the optimal path:" 
		print "From", beginning   # int to string
		for i in range(len(optimalOrder)):
			print ", go to ", path[i], ", pick up " ,optimalOrder[i]
		print ", go to destination " + str(destination) + ", then drop off items."
		print "Total distance traveled: ", num

	def nearestMatrix(self):                  # edit on April 29, 2018
		itemsID = self.itemsID
		grid = self.grid
		ItemP=[]
		for itemID in itemsID:
			ItemP.append(self.item_position(itemID))
		disMatrix = []
		for (itemA, positionA) in enumerate(ItemP):
			distanceA = []
			for (itemB, positionB) in enumerate(ItemP):
				if(itemA != itemB):
					distanceA.append(self.distance(positionA,positionB))
				else:
					distanceA.append('X')
			disMatrix.append(distanceA)
		return disMatrix

	def nearestNeighbor(self, disMatrix, beginItem):			# edit on April 29, 2018
		# dictItemP = {itemID, position}
		#disMatrix = self.nearestMatrix(grid,itemsID)
		order = []
		dis =0
		N = len(disMatrix)
		#print disMatrix
		line =beginItem
		order.append(line)
		for i in range(0,N):
			disMatrix[i][line] = 'X'
		for i in range(0,N-1):
			#print type(dis)
			#print (min(disMatrix[line]))
			dis += min(disMatrix[line])
			nextLine = disMatrix[line].index(min(disMatrix[line]))
			order.append(nextLine)
			for j in range(0,N):
				disMatrix[j][nextLine] = 'X'
			line = nextLine
		#print dis, order
		return dis, order

	def nnCost(self, order):			# edit on May 20, 2018
		itemsID = self.itemsID
		beginning = self.beginning
		destination = self.destination
		item_dimTab = self.item_dimTab 
		cost =0
		N = len(order)
		 # calculate cost from begin point to beginItem
		position = self.item_position(itemsID[order[0]])
		if (item_dimTab.has_key(itemsID[order[0]])):
			weight = item_dimTab[itemsID[order[0]]][3]
		else:
			weight = 1
		cost = cost + self.distance(beginning,position)*weight
		for i in range(0,N-1):
			positionA = self.item_position(itemsID[order[i]])
			positionB = self.item_position(itemsID[order[i+1]])
			if (item_dimTab.has_key(itemsID[order[i]])):
				weight += item_dimTab[itemsID[order[i]]][3]
			else:		
				weight += 1
			cost = cost + self.distance(positionA,positionB)*weight
		# calculate cost from end item to destination
		position = self.item_position(itemsID[order[N-1]])
		if (item_dimTab.has_key(itemsID[order[N-1]])):
			weight += item_dimTab[itemsID[order[N-1]]][3]
		else:
			weight += 1
		cost = cost + self.distance(position,destination)*weight
		return cost

	def nearNeiborInrtn(self, disMatrix, k):		# edit on April 29, 2018
		itemsID = self.itemsID
		#disN = []
		costN = []
		orderN = []
		OptimalItem = []
		for i in range(k):
			mydisMatrix = copy.deepcopy(disMatrix)
			dis, order = self.nearestNeighbor(mydisMatrix, i)
			if self.W == True:
				cost = self.nnCost(order)                 # add on May 20
			else:
				cost = dis
			#if (i==19):
			#	print"here"
			costN.append(cost)
			orderN.append(order)

		minD = min(costN)

		OptimalOrder = orderN[costN.index(minD)]
		for item in OptimalOrder:
			OptimalItem.append(itemsID[item])
		#print OptimalItem
		return OptimalItem, minD

	def nearNeighbor(self, beginning, destination, itemsID, k, W):		# edit on April 29, 2018
		grid = self.grid
		self.beginning = beginning
		self.destination = destination
		self.itemsID = itemsID
		self.W = W
		#start = time.clock()
		#hp = hpy()
		disMatrix=self.nearestMatrix()
		'''
		print itemsID
		print "optCost1"
		print "Distance matrix is: "
		for line in disMatrix:
			print line
		'''
		OptimalItem, optCost = self.nearNeiborInrtn(disMatrix,k)

		#optPath = self.gePath(beginning, destination, OptimalItem)
		#optDistance	= self.pathDist(optPath)	
		optDistance = 0
		#print grid[OptimalItem[0]]
		#print grid[OptimalItem[len(OptimalItem)-1]]
		#print i, optDistance
		#end = time.clock()
		#print "Time spent for generate nearestMatrix:", end-start
		#print disMatrix
		#print "Heap at the end of processing nearestMatrix :", hp.heap()
		return optCost, OptimalItem



