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

		self.__bombsFound = False
		self.__totalBombs = totalMines
		self.__curBombs = 0

		# self.__debug = 0
		
	def getAction(self, number: int) -> "Action Object":
		# if self.__debug == 20:
		# 	return Action(AI.Action.LEAVE)
		# self.__debug += 1

		# self.__printBoard()

		#NUMBER -> number of the last uncovered cell
		if number >= 0:
			self.__board[self.__lastX][self.__lastY] = number

		if self.__bombsFound:
			return self.__uncoverNextNotBomb() 

		a = self.__uncoverNextZero()
		if a != None:
			return a
		
		b = self.__checkAroundNonZero()
		if b != None:
			return b			
			
		#Take a guess if our algorithm has failed
		return self.__takeGuess()
	
	def __checkAroundNonZero(self):
		'''Either flags cells that must have remaining cells around as bombs,
		or uncovers cells that already have enouhg marked bombs around them.'''
		for numAtCell in range(1, 9):
			for i in range(self.__colDimension):
				for j in range(self.__rowDimension):
					if self.__board[i][j] == numAtCell:
						emptyCount = 0
						bombCount = 0
						newBomb = False
						for x in range(-1, 2):
							for y in range(-1,2):
								if (i +x < 0 or i + x >= self.__colDimension or j + y < 0 or j + y >= self.__rowDimension):
									continue
								if (self.__board[i + x][j + y] == -1):
									emptyCount += 1
									bx = i + x
									by = j + y
									newBomb = True
								if (self.__board[i + x][j + y] == 'b'):
									bombCount += 1
						
						if bombCount == numAtCell and emptyCount >= 1:
							action = AI.Action.UNCOVER
							self.__lastX = bx
							self.__lastY = by
							return Action(action, bx, by)
						
						if (emptyCount + bombCount) == numAtCell and not self.__bombsFound and newBomb:
							self.__curBombs += 1
							if self.__curBombs == self.__totalBombs:
								self.__bombsFound = True
							self.__board[bx][by] = 'b'
							action = AI.Action.FLAG
							return Action(action, bx, by)

	def __uncoverNextZero(self):
		'''Uncover anything around a 0 cell'''
		for i in range(self.__colDimension):
			for j in range(self.__rowDimension):
				#If cell is 0 uncover anything around it
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


	def __takeGuess(self):
		'''Take a guess or leave if you cannot'''
		guess = Action(AI.Action.LEAVE)	
		for i in range(self.__colDimension):
			for j in range(self.__rowDimension):
				if (self.__board[i][j] == -1):
					self.__lastX = i
					self.__lastY = j
					guess = Action(AI.Action.UNCOVER, i, j)
					

		return guess

	def __uncoverNextNotBomb(self):
		'''All bombs are found just uncover -1's'''
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
				# print('(', i, j, ')', end=' ')
			print()
		print('--------------------')