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
import itertools
from collections import Counter
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

		self.__lastMove = 0
		self.__sameMoveCounter = 0
		
	def getAction(self, number: int) -> "Action Object":
		if self.__lastMove == number:
			self.__sameMoveCounter += 1
		else:
			self.__sameMoveCounter = 0
		self.__lastMove = number
		if self.__sameMoveCounter >= 100:
			return Action(AI.Action.LEAVE)
		
		# if number == -2:
		# 	return Action(AI.Action.LEAVE)
		#NUMBER -> number of the last uncovered cell
		if number >= 0:
			self.__board[self.__lastX][self.__lastY] = number
		else:
			self.__board[self.__lastX][self.__lastY] = 'b'

		# self.__printBoard()

		if self.__bombsFound:
			return self.__uncoverNextNotBomb() 

		a = self.__uncoverNextZero()
		if a != None:
			return a
		
		b = self.__checkAroundNonZero()
		if b != None:
			return b		

		c = self.__futureMove()	
		if c != None:
			# print(c.getMove(), c.getX(), c.getY())
			return c	
		
		# d = self.__makeBetterGuess()
		# if d != None:
		# 	return d

		return self.__takeGuess()
		

	def __futureMove(self):
		def getEmptyCount(xPox, yPos):
			count = 0
			for x in range(-1, 2):
				for y in range(-1,2):
					if (xPos+x < 0 or xPos + x >= self.__colDimension or yPos + y < 0 or yPos + y >= self.__rowDimension):
						continue
					if (self.__board[xPos + x][yPos + y] == -1):
						count += 1
			return count
		def getBombCount(xPos, yPos):
			count = 0
			for x in range(-1, 2):
				for y in range(-1,2):
					if (xPos+x < 0 or xPos + x >= self.__colDimension or yPos + y < 0 or yPos + y >= self.__rowDimension):
						continue
					if (self.__board[xPos + x][yPos + y] in ('b', 't')):
						count += 1
			return count

		def getPossibleCells(xPos, yPos):
			if self.__board[xPos][yPos] in ('t', 'b') or self.__board[xPos][yPos] < 0:
				return []
			possibleCells = []
			canReturn = False
			
			for x in range(-1, 2):
				for y in range(-1,2):
					
					if (xPos+x < 0 or xPos + x >= self.__colDimension or yPos + y < 0 or yPos + y >= self.__rowDimension):
						continue
					if (self.__board[xPos + x][yPos + y] == -1):
						possibleCells.append([xPos + x, yPos + y])
					elif (self.__board[xPos + x][yPos + y] == 't'):
						canReturn = True

			if canReturn:
				return possibleCells	

			return []		

		for i in range(self.__colDimension):
			for j in range(self.__rowDimension):
				if self.__board[i][j] == 'b' or self.__board[i][j] <= 0:
					continue
				positions = []
				bombCount = 0
				
				for x in range(-1, 2):
					for y in range(-1,2):
						if (i + x < 0 or i + x >= self.__colDimension or j + y < 0 or j + y >= self.__rowDimension):
							continue
						if (self.__board[i + x][j + y] == -1):
							positions.append([i+x, j+y])
							
						if (self.__board[i + x][j + y] == 'b'):
							bombCount += 1
				if len(positions) > 0:
					combos = []
					for iteration in itertools.combinations(positions, self.__board[i][j] - bombCount):
						combos.append(iteration)

					for xPos in range(i-2, i+3):
						for yPos in range(j-2, j+3):
							
							if xPos < 0 or yPos < 0 or xPos >= self.__colDimension or yPos >= self.__rowDimension:
								continue
							info = []
							bTouching = []
							for combo in combos:
								for c in combo:
									self.__board[c[0]][c[1]] = 't'
								
								info.append(getPossibleCells(xPos, yPos))
								
								bTouching.append(getBombCount(xPos, yPos))

								for c in combo:
									self.__board[c[0]][c[1]] = -1
							if info == []:
								continue


							uniqueTouch = Counter(bTouching).keys()
							if len(uniqueTouch) != 1:
								continue

							final = []
							for positions in info:
								for pos in positions:
									final.append(pos)
							
							for point in final:
								if final.count(point) == len(info):
									if getEmptyCount(xPos, yPos) >= 5 and self.__board[xPos][yPos] == 2:
										continue

									if self.__board[xPos][yPos] - getBombCount(xPos, yPos) != 1 and bTouching[0] != self.__board[xPos][yPos]:
										self.__curBombs += 1
										if self.__curBombs == self.__totalBombs:
											self.__bombsFound = True
										action = AI.Action.FLAG
									else:
										action = AI.Action.UNCOVER
									self.__lastX = point[0]
									self.__lastY = point[1]
									return Action(action, point[0], point[1])

	
	def __checkAroundNonZero(self):
		'''Either flags cells that must have remaining cells around as bombs,
		or uncovers cells that already have enouhg marked bombs around them.'''
		# for numAtCell in range(1, 9):
		for i in range(self.__colDimension):
			for j in range(self.__rowDimension):
				# if self.__board[i][j] == numAtCell:
				if self.__board[i][j] == 'b' or self.__board[i][j] <= 0:
					continue
				numAtCell = self.__board[i][j]
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
					self.__lastX = bx
					self.__lastY = by
					self.__curBombs += 1
					if self.__curBombs == self.__totalBombs:
						self.__bombsFound = True
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
				if self.__board[i][j] == -1:
					print('-', end=' ')
				else:
					print(self.__board[i][j], end=' ')
				# print('(', i, j, ')', end=' ')
			print()
		print('--------------------')


	# def __makeBetterGuess(self):
	# 	'''Please try implementing this'''
	# 	pointDict = {}

	# 	def recursive():
	# 		# self.__printBoard()
	# 		for i in range(self.__colDimension):
	# 			for j in range(self.__rowDimension):
	# 				# print(i, j)
	# 				if self.__board[i][j] in ('b', 't') or self.__board[i][j] <= 1:
	# 					continue
	# 				positions = []
	# 				bombCount = 0
					
	# 				for x in range(-1, 2):
	# 					for y in range(-1,2):
	# 						if (i + x < 0 or i + x >= self.__colDimension or j + y < 0 or j + y >= self.__rowDimension):
	# 							continue
	# 						if (self.__board[i + x][j + y] == -1):
	# 							positions.append([i+x, j+y])
								
	# 						if (self.__board[i + x][j + y] in ('b', 't')):
	# 							bombCount += 1

	# 				if len(positions) > 0:
	# 					combos = []
	# 					for iteration in itertools.combinations(positions, self.__board[i][j] - bombCount):
	# 						combos.append(iteration)
						
	# 					for combo in combos:
	# 						for c in combo:
	# 							self.__board[c[0]][c[1]] = 't'
	# 							recursive()
	# 							spot = str(c[0]) + " " + str(c[1])
	# 							if spot in pointDict:
	# 								pointDict[spot] += 1
	# 							else:
	# 								pointDict[spot] = 1
								
	# 							self.__board[c[0]][c[1]] = -1
	# 	recursive()
	# 	print("SHOW ME")