#EECS 221 Adv App Algorithms
#Project name: Project week7
#Author: Yuanzhe Li
#Student ID: 14563990
#Date: May/20/2018
#Language: Python 2.7
#Algorithm

import os
import csv
import re
import time
#from guppy import hpy
import copy
import heapq 
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from Tkinter import *
import tkFileDialog
from nearNeighbor import NN
from branchBound import BB

class warehouse():

	def __init__(self):
		self.beginning = [1,1]
		self.destination = [19,19]
		self.mode = 0
		self.algorithm =0
		self.maxWeight =0
		self.order =0
		self.orderPath =""
		self.defaultWeight = 50
		self.itemsID = []
		#self.nnOrder = []
		#self.BBOrder = []
		#self.upperBound = sys.maxint
		#self.orderHeap = []

	def readcsv(self):
		pass

	def build_grid(self):
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

	def build_tab(self):
		item_dimTab = {}
		if False == os.path.isfile('item-dimensions-tabbed.txt'):
			print "item-dimensions-tabbed.txt is not exist."
			return 0
		with open( 'item-dimensions-tabbed.txt', 'rb') as f:
			f.readline()
			for row in f.readlines():
				ID,legth,width,height,weight = row.split()
				item_dimTab[ID] = [legth,width,height,weight]
				#print item_dimTab[ID][3]
		f.close()
		return item_dimTab

	def items_position(self, grid, itemsID):    # return a dict of a list of itemID with position
		dictItemP = {}
		for itemID in itemsID:
			dictItemP[itemID] = self.item_position(grid, itemID)
		return dictItemP

	def items_distance(self):
		pass



	def lowerBound(self, disMatrix):

		return 
	def findPath(self, grid, beginning, destination, itemsID):
		
		dictItemP = self.items_position(grid, itemsID)
		toDntion = {}
		toBegin = {}
		optimalOrder =[]
		optDistance =0

		for (itemID, position) in dictItemP.items():
			toDntion[itemID] = (self.distance(destination,position))

		for (itemID, position) in dictItemP.items():
			toBegin[itemID] =  (self.distance(beginning,position))

		toDntion = sorted(toDntion.items(), key = lambda d: d[1])
		toBegin = sorted(toBegin.items(), key = lambda d: d[1])

		if(toDntion[0][1] < toBegin[0][1]):    # smallest distance near destination
			toDntion = sorted(toDntion, key = lambda d: d[1], reverse= True )
			for item in toDntion:
				optimalOrder.append(item[0])
		else:
			for item in toBegin:
				optimalOrder.append(item[0])
	
		optPath = self.gePath(grid, beginning, destination, optimalOrder)	
		optDistance	= self.pathDist(optPath)	
		return optimalOrder, optPath, optDistance

	def drawMap(self):
			pass

	def runGUI(self):
		grid = self.build_grid()
		item_dimTab = self.build_tab()
		bb = BB(grid, item_dimTab)
		nn = NN(grid, item_dimTab)


		root = tk.Tk()
		root.title('EECS221 Warehouse.' )
		root.wm_geometry("1200x800")


		leftFrame = Frame(root)
		leftFrame.pack(padx=20, side = LEFT)
		rightFrame = Frame(root)
		rightFrame.pack(padx=20, side = RIGHT)
		rightFrame.config(highlightbackground='grey')
		#rightFrame.wm_geometry("200x300")

		welcome = tk.Label(leftFrame, text='Welcome to warehouse system!', width=25)
		welcome.pack(side =TOP)

		# left side option
		def get_mode():
			self.mode = var1.get()
		    #labelR1.config(text='you have selected '+var.get())

		    #1. mode
		var1=tk.StringVar()
		labelR1=tk.Label(leftFrame,bg='grey',width=20,text='1. Choose processing type:')
		labelR1.pack()

		r1=tk.Radiobutton(leftFrame,text='(A)Type in items',variable=var1,value='A',command=get_mode)
		r1.pack()
		r2=tk.Radiobutton(leftFrame,text='(B)Batch processing of orders',variable=var1,value='B',command=get_mode)
		r2.pack()
		r3=tk.Radiobutton(leftFrame,text='(C)Processed order',variable=var1,value='C',command=get_mode)
		r3.pack()


		def get_algorithm():
			self.algorithm = var2.get()
		    #labelR1.config(text='you have selected '+var.get())

		tk.Label(leftFrame,bg='white',width=20,text='').pack()
		    #2.algorithm
		var2=tk.StringVar()
		labelR2=tk.Label(leftFrame,bg='grey',width=20,text='2. Choose Algorithm:')
		labelR2.pack()

		r1=tk.Radiobutton(leftFrame,text='(A)Near Neighbor',variable=var2,value='A',command=get_algorithm)
		r1.pack()
		r2=tk.Radiobutton(leftFrame,text='(B)Branch & Bound',variable=var2,value='B',command=get_algorithm)
		r2.pack()

		def get_weight():
			self.considerWeight = var3.get()
		tk.Label(leftFrame,bg='white',width=20,text='').pack()
            #3.weight
		var3=tk.StringVar()
		labelR3=tk.Label(leftFrame,bg='grey',width=20,text='3. Consider items weight? :')
		labelR3.pack()

		r1=tk.Radiobutton(leftFrame,text='(A)Yes',variable=var3,value=True,command=get_weight)
		r1.pack()
		r2=tk.Radiobutton(leftFrame,text='(B)No',variable=var3,value=False,command=get_weight)
		r2.pack()

		def begin_end():
			beginEnd = var4.get().split(' ')
			self.beginning = eval(beginEnd[0])
			self.destination = eval(beginEnd[1])
            #4. begin, end
		var4 = tk.StringVar()
		tk.Label(leftFrame,bg='white',width=20,text='').pack()
		labelR4=tk.Label(leftFrame,bg='grey',width=20,text='4. Type in begin end point :')
		labelR4.pack()
		beginEndPoint = Entry(leftFrame, width = 15, borderwidth = 3, relief = 'sunken', textvariable=var4)
		beginEndPoint.pack()
		beginEndPoint.get()

		def setWeight():
			self.maxWeight = eval(var5.get())
		var5 = tk.StringVar()
            #5. weight
		labelR5=tk.Label(leftFrame,bg='grey',width=20,text='5. Type in max weight :')
		labelR5.pack()
		maxWight = Entry(leftFrame, width = 15, borderwidth = 3, relief = 'sunken', textvariable=var5)
		maxWight.pack()
		maxWight.get()

		def setItemsID():
			self.itemsID = eval(var6.get())

		var6 = tk.StringVar()
            #6. order
		tk.Label(leftFrame,bg='white',width=20,text='').pack()
		labelR6=tk.Label(leftFrame,bg='grey',width=20,text='6. Type in order/# here :')
		labelR6.pack()
		order = Entry(leftFrame, width = 40, borderwidth = 3, relief = 'sunken', textvariable=var6)
		order.pack()
		#order.get()

        #7. upload orders

		def openfile():
			path = os.getcwd()
			#print path
			r = tkFileDialog.askopenfilename(title='Open file. ', initialdir=path,
                                             filetypes=[('Python', '*.py *.pyw'), ('All Files', '*')])
			self.orderPath = r
			print r
		tk.Label(leftFrame,bg='white',width=20,text='').pack()
		labelR7=tk.Label(leftFrame,bg='grey',width=20,text='7. Upload orders/res here :')
		labelR7.pack()
		#b = Button(... command = lambda: button('hey'))
		btn1 = tk.Button(leftFrame, text='Upload orders', command=openfile)
		btn1.pack()


		#8. process
		def process():
			begin_end()     # record begin end point
			setWeight()
			setItemsID()    # if type in by hand
			weightNow = 0
			if self.mode == 'A' :
				#if self.algorithm == 'A':   # near neighbor
					# check max weight and order split
				itemsID = self.itemsID
				itemsNow =[]
				thisWeight = 1
				k = 0
				for item in itemsID:
					k++
					if (item_dimTab.has_key(item)):
						thisWeight = item_dimTab[item][3]
					else:
						thisWeight = 1

					if(weightNow + thisWeight>self.maxWight or k == len(itemsID)):
						if self.algorithm == 'A':  # choose algorithm
							optCost, OptimalItem = nn.nearNeighbor(self.beginning, self.destination, itemsNow, len(itemsNow),self.considerWeight)
							logStr = "near neighbor process. \n"
							txt.insert(END, logStr)
							#self.drawMap(OptimalItem)
						else :
							cost, order = bb.branchBound(self.beginning, self.destination, itemsNow,self.considerWeight)
							logStr = " branch bound process. \n"
							txt.insert(END, logStr)
							#self.drawMap(OptimalItem)

						logStr = "Order splits because of over weight. This trip contains items: ", itemsNow, "\n"
						txt.insert(END, logStr)
						itemsNow =[].append(item)
						weightNow = 0
					else:
						itemsNow.append(item)
					weightNow += thisWeight

			else if self.mode == 'B':              # batch processing
				logStr = "batch processing...... \n"
				txt.insert(END, logStr)
				fileName = self.orderPath
				if (fileName == ""):                  # No orders path input 
					logStr = "No orders path...... \n"
					txt.insert(END, logStr)
					return 0
				else: 
					outputList = []
					with open( fileName, 'rb') as f:
						lines = f.readlines()
						for line in lines:
							line = line.split('\t')
							while '' in line:
								line.remove('')
							while '\r\n' in line:
								line.remove('\r\n')
							#print line
							itemsID =line
							itemsID = map(int, itemsID)
							itemsID = set(itemsID)
							itemsID = list(itemsID)
							self.itemsID = itemsID
							#print itemsID
							# near neighbor
							optCost, OptimalItem = nn.nearNeighbor(self.beginning, self.destination, self.itemsID, len(self.itemsID),self.considerWeight)
							#self.drawMap(OptimalItem)
							logStr = "near neighbor process finish. \n"
							txt.insert(END, logStr)
							# branch bound
							cost, order = bb.branchBound(self.beginning, self.destination, self.itemsID,self.considerWeight)
							#self.drawMap(order)
							logStr = " branch bound process finish. \n"
							txt.insert(END, logStr)	
							outputRow = (self.beginning, self.destination,self.itemsID,OptimalItem,optCost,order,cost)
							outputList.append(outputRow)	
					f.close()
					# output result to file
					fileName2 = 'warehouseOutput.txt'
					with open( fileName2, 'wb') as f2:
						writer = csv.writer(f2)
						writer.writerows(outputList)
					f2.close()
					logStr = " Batch processing of orders finish. \n"
					txt.insert(END, logStr)	
					print "Finish Batch processing of orders."					

			else:          # mode = C  read processed order
				print "self.itemsID is: ", type(self.itemsID)
				orderNumber = self.itemsID
				fileName = self.orderPath
				i = 1
				if(orderNumber<1):
					logStr = "order number is smaller than 1, using default number: 1. \n"
					txt.insert(END, logStr)
					orderNumber = 1
				if (fileName == ""):                  # No orders path input 
					logStr = "No orders path...... \n"
					txt.insert(END, logStr)
					return 
				else: 
					intputList = []
					with open( fileName, 'rb') as f:
						lines = f.readlines()
						for line in lines:
							if(i == orderNumber):
								c = eval(line) # content in one line
								self.beginning = list(c[0])
								self.destination = list(c[1])
								self.itemsID = list(c[2])
								nnOrder = list(c[3])
								nnCost = int(c[4])
								bbOrder = int(c[5])
								bbCost = int(c[6])
								logStr = "For order ", i, ". The start location is: ", self.beginning, " End location is: ", self.destination
								txt.insert(END, logStr)
								logStr = "Original order: ", self.itemsID, ". nn Optimal order: ", nnOrder, " Cost: ", nnCost
								txt.insert(END, logStr)
								logStr = "Original order: ", self.itemsID, ". bb Optimal order: ", bbOrder, " Cost: ", bbCost
								txt.insert(END, logStr)
								break
								#self.drawMap()
					f.close()

			txt.insert(END, "\n End process. \n")

		tk.Label(leftFrame,bg='white',width=20,text='').pack()
        #labelR7=tk.Label(leftFrame,bg='grey',width=20,text='6. Upload orders here :')
        #labelR7.pack()
        #b = Button(... command = lambda: button('hey'))
		btn2 = tk.Button(leftFrame, text='Pocessing!', command=process)
		btn2.pack()



        #9. Result


		tk.Label(leftFrame,bg='white',width=20,text='').pack()
            # create a Frame for the Text and Scrollbar
		txt_frm = tk.Frame(leftFrame, width=200, height=120)
		txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
		txt_frm.grid_propagate(False)
         # implement stretchability
		txt_frm.grid_rowconfigure(0, weight=1)
		txt_frm.grid_columnconfigure(0, weight=1)
        # create a Text widget
		txt = tk.Text(txt_frm, borderwidth=1)
		txt.config(font=("consolas", 12), undo=True, wrap='word')
		txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        # create a Scrollbar and associate it with txt
		scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
		scrollb.grid(row=0, column=1, sticky='nsew')
		txt['yscrollcommand'] = scrollb.set
		txt.insert(END, "Result txt box. \n")

		#9.  Delete Button
		btn3 = Button(leftFrame, text='Clear All', command=lambda: txt.delete(1.0,END))
		btn3.pack()
		'''
		go_button = tk.Button(right, text='Quit!', width=3, height=1, command=root.destroy)
		go_button.pack(side="top")
		'''
		l = []
		height = 30
		width = 30
		for i in range(height): #Rows
			for j in range(width): #Columns
                #my_test = tk.Label(leftFrame, text='Quit!', width=1)
				if((i+1)%2 ==0  and (j+1)%2 ==0 ):
					Label(rightFrame, text="    ", bg='black').grid(row =i,column =j)
				else:
					Label(rightFrame, text="    ", bg='white').grid(row=i, column=j)

		root.mainloop()




	def runCMD(self):
		#data = self.readcsv()
		grid = self.build_grid()
		beginning = [1,1]
		destination =[20,20]
		item_dimTab = self.build_tab()

		W = True
		bb = BB(grid, item_dimTab)
		nn = NN(grid, item_dimTab)
		print 'Welcome to warehouse grid system!'

		while True:
			choose =0
			print ''
			print ''
			beginning = eval(raw_input('Hello User, where is your worker?:'))
			print 'Worker begin at: ', beginning
			destination = eval(raw_input('\nWhat is your workers end location?'))
			print 'Worker end at: ', destination
			while(choose == 0):
				choose = eval(raw_input('\nDo you want to (1)type in items by yourself or (2)Batch processing of orders\n?'))
				choose2 = eval(raw_input('\nWitch Algorithm you want to use (1)Near Neighbor or (2)Branch & Bound\n?'))
				choose3 = eval(raw_input('\nConsider items weight? (1)Yes (2)No\n?'))
				if(choose ==1):
					itemsID = eval(raw_input('\nHello User, what items would you like to pick?:'))
					print '\nItems ID is: ', itemsID
					k = len(itemsID)
					if(choose2 == 1 and choose3 == 1):      # Near Neighbor Algorithm, Consider weight 
						W = True
						print "Near Neighbor Algorithm, Consider weight : "
						print "Calculating ......"
						optCost, OptimalItem = nn.nearNeighbor(beginning, destination, itemsID, k,W)
						print 'Optimal Cost is: ',optCost
						print 'Optimal Item order is: ', OptimalItem

					elif(choose2 == 2 and choose3 == 1):     # Branch & Bound, Consider weight 
						W = True
						print "Branch & Bound, Consider weight  : "
						print "Calculating ......"
						cost, order = bb.branchBound(grid,item_dimTab, beginning, destination, itemsID,W)
						print 'Optimal Cost is: ',cost
						print 'Optimal Item order is: ', order

					elif(choose2 == 1 and choose3 == 2):	# Near Neighbor Algorithm, No Consider weight
						W = False
						print "Near Neighbor Algorithm, No Consider weight : "
						print "Calculating ......"
						optCost, OptimalItem = nn.nearNeighbor(beginning, destination, itemsID, k,W)
						print 'Optimal Cost is: ',optCost
						print 'Optimal Item order is: ', OptimalItem

					elif(choose2 == 2 and choose3 == 2):	# Branch & Bound, No Consider weight
						W = False
						print "Branch & Bound, No Consider weight  : "
						print "Calculating ......"
						cost, order = bb.branchBound(grid,item_dimTab, beginning, destination, itemsID,W)
						print 'Optimal Cost is: ',cost
						print 'Optimal Item order is: ', order

				elif (choose ==2):
				# Worker Start Location, Worker end Location, Original Parts Order
				# Optimized Parts Order, Original Parts Total Distance, Optimized Parts Total Distance
					fileName = 'warehouse-orders-v02-tabbed.txt'
					outputList = []
					with open( fileName, 'rb') as f:
						lines = f.readlines()
						for line in lines:
							line = line.split('\t')
					 		while '' in line:
					 			line.remove('')
					 		while '\r\n' in line:
					 			line.remove('\r\n')
							#print line
							itemsID =line
							itemsID = map(int, itemsID)
							itemsID = set(itemsID)
							itemsID = list(itemsID)
							k = len(itemsID)
							#print itemsID
							if(choose2 == 1 and choose3 == 1):      # Near Neighbor Algorithm, Consider weight 
								W = True
								Order, Cost = nn.nearNeighbor(beginning, destination, itemsID, k,W)
							elif(choose2 == 2 and choose3 == 1):     # Branch & Bound, Consider weight 
								W = True
								Cost, Order = bb.branchBound(grid,item_dimTab, beginning, destination, itemsID,W)

							elif(choose2 == 1 and choose3 == 2):	# Near Neighbor Algorithm, No Consider weight
								W = False
								Order, Cost = nn.nearNeighbor(beginning, destination, itemsID, k,W)
				
							elif(choose2 == 2 and choose3 == 2):	# Branch & Bound, No Consider weight
								W = False
								Cost, Order = bb.branchBound(grid,item_dimTab, beginning, destination, itemsID,W)
							
							outputRow = (beginning, destination,itemsID,Order,Cost)
							outputList.append(outputRow)

					f.close()

					fileName2 = 'warehouseOutput.txt'
					with open( fileName2, 'wb') as f2:
						writer = csv.writer(f2)
						writer.writerows(outputList)
					f2.close()
					print "Finish Batch processing of orders."
				else:
					choose = 0
					print "Type wrong option, try again."

	def test2(self):		# edit on April 29, 2018

		grid = self.build_grid()
		beginning = [1,1]
		destination =[20,20]
		item_dimTab = self.build_tab()
		#itemsID = [46071, 379019,70172,1321,2620261]
		#itemsID = [2625154, 1019019, 100382, 154720, 299576]
		#itemsID = [1651829, 2253198, 1622191, 1621045, 1621158, 1622196, 1622195, 1622191, 1945580, 1628756, 1629090, 2625541, 2625537, 1623864, 1622038, 1621964, 1624694, 1626710, 1626709, 1626718]
		
		# 17 items
		itemsID = [231434, 286783, 274852, 49524, 170758, 76182, 264804, 1456044, 108775, 380552, 227318, 408295, 408451, 308223, 59538, 348200, 1101294]
		#itemsID = [231434, 286783, 274852, 49524, 170758, 76182, 264804, 1456044, 108775, 380552, 227318, 408295, 408451, 308223]
		k = len(itemsID)
		W = True
		bb = BB()
		#OptimalItem, optPath, optDistance = self.NN(grid, beginning, destination, itemsID, k)
		cost, order = bb.branchBound(grid,item_dimTab, beginning, destination, itemsID,W)
		#print '[46071, 379019,70172,1321,2620261] Optimal Distance is: ',optDistance-14
		#print OptimalItem, optPath, optDistance	
	def test4(self):		# edit on April 29, 2018

		grid = self.build_grid()
		item_dimTab = self.build_tab()
		beginning = [1,1]
		destination =[20,20]
		W = True
		itemsID = [46071, 379019,70172,1321,2620261]
		#itemsID = [2625154, 1019019, 100382, 154720, 299576, 817287, 336712, 1734057, 82591, 259577]
		k = len(itemsID)
		nn = NN(grid, item_dimTab)
		OptimalItem, optCost = nn.nearNeighbor(beginning, destination, itemsID, k,W)
		#cost, order = self.branchBound(grid, beginning, destination, itemsID)
		print '[46071, 379019,70172,1321,2620261] Optimal Cost is: ',optCost
		print 'Optimal Item order is: ', OptimalItem


if __name__ == '__main__':
	try:
		ware = warehouse()
		#ware.test4()
		ware.runGUI()
		#ware.run()
	except KeyboardInterrupt as e:
		print('\nExit.')
	except Exception as e:
		print(e)

