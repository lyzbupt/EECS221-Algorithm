#EECS 221 Adv App Algorithms
#Project name: Project week7
#Author: Yuanzhe Li
#Student ID: 14563990
#Date: May/20/2018
#Language: Python 2.7
# Greedy Algorithm

import os
import csv
import re
import time
#from guppy import hpy
import copy
import heapq 
import sys
from nearNeighbor import NN

class BB():
	def __init__(self, grid , item_dimTab):
		self.upperBound = sys.maxint
		self.orderHeap = []
		self.finalOrder = []
		self.finalCost  = 0
		self.itemsID = []
		self.beginning = []
		self.destination = []
		self.item_dimTab = item_dimTab
		self.grid=grid

	def clearAll(self):
		self.upperBound = sys.maxint
		self.orderHeap = []
		self.finalOrder = []
		self.finalCost  = 0
		self.itemsID = []
		self.beginning = []
		self.destination = []
		#self.item_dimTab = []
		#self.grid=[]

	def item_position(self, itemID):    # return item positon in coordination
		grid = self.grid
		return grid[itemID]

	def distance(self, posN1, posN2):			# return distance between two positions
		return (abs(posN1[0]-posN2[0])+abs(posN1[1]-posN2[1]))

	def process(self):  # edit on May 13, 2018
		orderHeap = self.orderHeap
		cost, order, tempMatrix = heapq.heappop(orderHeap)
		#print tempMatrix
		src = order[len(order)-1]
		if(len(order)== len(tempMatrix)):
			cost += tempMatrix[src][0]

			if(cost<self.upperBound):
			# change upperbound
			#....
				self.upperBound = cost
				self.finalOrder = order
				self.finalCost  = cost
			return cost, order

		if(cost>= self.upperBound):
			return cost, order

		rowX =[]
		for i in range(len(tempMatrix)):
			rowX.append('X')
		#leafValue =[]
		content = []
		for i in range(len(tempMatrix)):
			cost1 = cost
			content = []
			tempMatrix1 = copy.deepcopy(tempMatrix)
			if(tempMatrix[src][i]!='X' and (i != 0)):
				cost1+=tempMatrix[src][i]
				# set src row -> inf
				tempMatrix1[src] = rowX
				# set dest col -> inf
				for j in range(len(tempMatrix)):
					tempMatrix1[j][i] = 'X'
				# set dest src -> inf
				tempMatrix1[i][src] = 'X'
				# add leaf to Map
				cost1+=self.reduceMatrix(tempMatrix1)
				if(cost1<self.upperBound):
					#leafValue.append(cost1)
					content.append(cost1)
					newOrder = copy.deepcopy(order)
					newOrder.append(i)
					content.append(newOrder)
					content.append(tempMatrix1)
					heapq.heappush(orderHeap, content)
					'''
					print cost1, newOrder
					for i in tempMatrix1:
						print i
					print ''
					'''
		return cost, order


	def reduceMatrix (self, disMatrix):						# edit on May 6, 2018
		value = 0
		# row
		for line in disMatrix:
			minValue = min(line)
			if (minValue>0 and minValue<'X'):
				value += minValue
				for i in range(len(line)):
					if(line[i] != 'X'):
						line[i] -= minValue
		# col
		for i in range(len(disMatrix)):
			col =[]
			for j in range(len(disMatrix)):
				col.append(disMatrix[j][i])
			minValue = min(col)
			if (minValue>0 and minValue<'X'):
				value += minValue
				for j in range(len(disMatrix)):
					if(disMatrix[j][i] != 'X'):
						disMatrix[j][i] -= minValue
		return value

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


	def branchBound(self,beginning, destination, itemsID, W): # edit on May 13, 2018
		self.clearAll()
		self.itemsID = itemsID
		self.beginning = beginning
		self.destination = destination
		orderHeap = self.orderHeap
		value = 0
		ItemP = []
		rowX =[]
		if (len(itemsID)==1):
			if(W==True):
				cost = self.nnCost([0])
				#print "Cost with weight is : ", cost
				return cost, itemsID
			else:
				cost = self.nnCost([0])
				#print "Cost with weight is : ", cost
				return cost, itemsID

		for i in range(len(itemsID)+1):
			rowX.append('X')
		ItemP.append(beginning)
		for itemID in itemsID:
			ItemP.append(self.item_position(itemID))
		disMatrix = []
		for (indexA, positionA) in enumerate(ItemP):
			distanceA = []
			for (indexB, positionB) in enumerate(ItemP):
				if(indexA != indexB):
					distanceA.append(self.distance(positionA,positionB))
				else:
					distanceA.append('X')
			disMatrix.append(distanceA)
		for i in range(len(disMatrix)):
			if (i != 0):
				disMatrix[i][0] = self.distance(ItemP[i],destination)    # init, create distance matrix
		value+=self.reduceMatrix (disMatrix)         # init value
		cost =value
		content = []
		order =[0]
		tempMatrix = disMatrix
		content.append(cost)
		content.append(order)
		content.append(tempMatrix)
		heapq.heappush(orderHeap, content)
		'''
		print value
		for i in disMatrix:
			print i
		print ''
		'''
		firstTime = time.clock()
		while True:
			# check time 
			if (time.clock() - firstTime >=10):         # order otems is too large
				print "Execution time is more than 30 s."
				if ( self.upperBound == sys.maxint ):
					print "Get no result, untouch leaf. "
					nn = NN(self.grid, self.item_dimTab)
					optCost, OptimalItem = nn.nearNeighbor(beginning, destination, itemsID, len(itemsID),W)
					return optCost, OptimalItem
				else:
					order = self.finalOrder
					cost  = self.finalCost
				break

			cost, order = self.process()
		#	print "first ", cost, order 
			if(len(orderHeap) <= 0):
				break
		order = self.finalOrder
		cost  = self.finalCost
		newOrder=[]
		newOrder.append(beginning)
		for i in range(1, len(ItemP)):
			newOrder.append(ItemP[order[i]])
		items =[]
		for i in range(1, len(ItemP)):
			items.append(itemsID[order[i]-1])
		print "Pick up order based on position: ", newOrder
		print "Pick up order based on items ID: ", items
		print "Total distance is : ", cost
		if (W == True):
			order.remove(0)
			neworder = [i-1 for i in order]
			cost = self.nnCost(neworder)
			print "Cost with weight is : ", cost
		return cost, items
