import time
import copy

class Puzzle:
	history = []
	LEFT = 'L'
	RIGHT = 'R'
	UP = 'U'
	DOWN = 'D'
	max = []
	matrix = []
	
	def __init__(self,matrix):
		self.solutions = []
		self.history = []
		self.matrix = copy.deepcopy(matrix)
		self.max = [len(self.matrix) - 1, len(self.matrix[0]) - 1]
	
	def __repr__(self):	
		return str(self.matrix)
	
	def getPossibleDirections(self):
		directions = [];
		for direction in [self.UP,self.DOWN,self.LEFT,self.RIGHT]:
			if self.canGo(direction):
				directions.append(direction)
		return directions	
	
	def isCompleted(self):
		for line in self.matrix:
			for element in line:
				if(element == 0):
					return 0
		return 1
	
	def canGo(self,direction):
		if direction == self.UP:
			result = ((self.pos[0] - 1) >= 0) and (self.matrix[self.pos[0] - 1][self.pos[1]] == 0)
		elif direction == self.DOWN:
			result = ((self.pos[0] + 1) <= self.max[0]) and (self.matrix[self.pos[0] + 1][self.pos[1]] == 0)
		elif direction == self.LEFT:
			result = ((self.pos[1] - 1) >= 0) and (self.matrix[self.pos[0]][self.pos[1] - 1] == 0)
		elif direction == self.RIGHT:
			result = ((self.pos[1] + 1) <= self.max[1]) and (self.matrix[self.pos[0]][self.pos[1] + 1] == 0)
		return result	
		
	def go(self,direction):
		self.history.append(direction)
		while self.canGo(direction):
			if direction == self.UP:
				self.pos[0] -= 1
			elif direction == self.DOWN:
				self.pos[0] += 1
			elif direction == self.LEFT:
				self.pos[1] -= 1
			elif direction == self.RIGHT:
				self.pos[1] += 1
			self.matrix[self.pos[0]][self.pos[1]] = 1			
	
	def branch(self):
		child = Puzzle(self.matrix)
		child.history = copy.deepcopy(self.history)
		child.pos = copy.deepcopy(self.pos)
		
		return child
		
	def start(self, pos, direction1 = 0):
		self.pos = pos
		
		if(self.matrix[self.pos[0]][self.pos[1]] == 1 and direction1 == 0):
			return 0
		
		self.matrix[pos[0]][pos[1]] = 1
		
		while 1:
			if direction1 == 0:
				possibleDirections = self.getPossibleDirections()
			else:
				possibleDirections = [direction1]
				direction1 = 0
			if len(possibleDirections) == 0:
				if self.isCompleted():
					self.solutions.append(self.history)
					return self.solutions
				else:
					if len(self.solutions) > 0:
						return self.solutions
					else:
						return 0
		
			directionCount = 0
			child = self.branch()
			for direction in possibleDirections:
				if directionCount == 0:
					self.go(direction)
				else:
					child1 = child.branch()
					r = child1.start(child1.pos,direction)
					if r != 0:
						self.solutions = self.solutions + child1.solutions
				directionCount += 1
	
	def findSolutions(matrix):
		for line in range(len(matrix)):
			for col in range(len(matrix[0])):
				p = Puzzle(matrix)
				if p.start([line,col]):
					print str(line) + " " + str(col) + " " + str(p.solutions)
				
	findSolutions = staticmethod(findSolutions)
				
if __name__ == "__main__":
	matrix = [[0,0,1,1,0],
			[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0],
			[1,1,1,0,0]]
			
	Puzzle.findSolutions(matrix)
				
