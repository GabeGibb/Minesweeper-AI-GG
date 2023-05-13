# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action

import random
class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.__board = []
		for i in range(colDimension):
			self.__board.append([])
			for _ in range(rowDimension):
				self.__board[i].append(-1)
		self.__board[startX][startY] = 0
		self.__lastX = startX
		self.__lastY = startY

		self.__bombFound = False
		#Create a 2D array of same dimension
		#Make everyting -1 for uncovered
		#0-any number for covered
		#Uncover every cell next to a 0
		#If we cannot do that, find a 1 with 1 remaining neighbor (this will be the bomb)
			#can mark a bomb with like -2 or a letter even
		#OR choose a random remaining cell to uncover

		
		
	def getAction(self, number: int) -> "Action Object":
		#NUMBER -> number of the last uncovered cell
		if number >= 0:
			self.__board[self.__lastX][self.__lastY] = number

		# self.__printBoard()
		if self.__bombFound:
			return self.__uncoverNextNotBomb() 

		for i in range(self.__colDimension):
			for j in range(self.__rowDimension):
				if self.__board[i][j] == 0:
					for x in range(-1, 2):
						for y in range(-1,2):
							if (i +x < 0 or i + x >= self.__colDimension or j + y < 0 or j + y >= self.__rowDimension):
								continue
							
							if (self.__board[i + x][j + y] == -1):
								action = AI.Action.UNCOVER
								self.__lastX = i + x
								self.__lastY = j + y
								return Action(action, i + x, j + y)
				
				if self.__board[i][j] == 1:
					count = 0
					for x in range(-1, 2):
						for y in range(-1,2):
							if (i +x < 0 or i + x >= self.__colDimension or j + y < 0 or j + y >= self.__rowDimension):
								continue
							if (self.__board[i + x][j + y] == -1):
								count += 1
								bx = i + x
								by = j + y
					
					if count == 1 and not self.__bombFound:
						self.__bombFound = True
						self.__board[bx][by] = 'b'
						action = AI.Action.FLAG
						return Action(action, bx, by)
						
		#Take a guess if our algorithm has failed
		guess = Action(AI.Action.LEAVE)	
		for i in range(self.__colDimension):
			for j in range(self.__rowDimension):
				if (self.__board[i][j] == -1):
					guess = Action(AI.Action.UNCOVER, i, j)

		return guess
	

	def __uncoverNextNotBomb(self):
		for i in range(self.__colDimension):
			for j in range(self.__rowDimension):
				if (self.__board[i][j] == -1):
					action = AI.Action.UNCOVER
					self.__lastX = i
					self.__lastY = j
					return Action(action, i, j)
		return Action(AI.Action.LEAVE)

	def __printBoard(self):
		for j in range(self.__rowDimension - 1, -1, -1):
			for i in range(self.__colDimension):
				print(self.__board[i][j], end=' ')
				print('(', i, j, ')', end=' ')
			print()
		print('--------------------')