# Artifical Intelligence @ edX
# Week4 Project
# Adversial Search and Games : 2048
# Renjie Li, rl2932@columbia.edu

from random import randint
from BaseAI import BaseAI
import time
import numpy
import math


class PlayerAI(BaseAI):



    def getMove(self, grid):
        self.start_time = time.clock()  # To prevent timeout
        moves = grid.getAvailableMoves()
        best_move = None # What we need to return
        MAX = -numpy.inf # The root is a MAX node, so we need to set the default MAX to -infinity
        for step in moves:
            child = grid.clone() # Deepcopy
            child.move(step)
            score = self.Minimax(child,method='Min')
            if score > MAX:
               MAX = score
               best_move = step
        return best_move


    def Minimax(self,grid,method):
        self.depth = 4
        if method == 'Min':
            return self.Min(grid)
        else:
            return self.Max(grid)

    def Min(self,grid):
        # Find the minimum evaluation(heuristic) for the computerAI
        if time.clock() - self.start_time > 0.04 or self.depth ==0:
            return self.Heuristic(grid)

        AvailableCells = grid.getAvailableCells() # Return coordinate like [0,1],[1,1]
        Min = numpy.inf
        children = []
        tile = [2,4]
        for cell in AvailableCells:
            for content in tile:
                temp = grid.clone()
                temp.insertTile(cell,content)
                children.append(temp)

        for child in children:
            self.depth -= 1
            MaxReturn = self.Max(child)
            if MaxReturn < Min:
                Min = MaxReturn

        return Min

    def Max(self,grid):
        # Find the maximum evaluation(heuristic) for the playerAI
        if time.clock() - self.start_time > 0.04 or self.depth==0 :
            return self.Heuristic(grid)

        AvailableMoves = grid.getAvailableMoves()
        Max = -numpy.inf
        children = []
        for move in AvailableMoves:
            child = grid.clone()  # Deepcopy
            child.move(move)
            children.append(child)

        for child in children:
            self.depth -= 1
            MinReturn = self.Min(child)
            if MinReturn > Max:
                Max = MinReturn

        return Max




    def Heuristic(self,grid):
        if grid.canMove() == False:
            return -numpy.inf

        gradients = [
            [[3, 2, 1, 0], [2, 1, 0, -1], [1, 0, -1, -2], [0, -1, -2, -3]],
            [[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, -0]],
            [[0, -1, -2, -3], [1, 0, -1, -2], [2, 1, 0, -1], [3, 2, 1, 0]],
            [[-3, -2, -1, 0], [-2, -1, 0, 1], [-1, 0, 1, 2], [0, 1, 2, 3]]
        ]

        values = [0,0,0,0]

        for i in range(4):
            for x in range(4):
                for y in range(4):
                    values[i] += gradients[i][x][y] * grid.map[x][y]


        return max(values)
