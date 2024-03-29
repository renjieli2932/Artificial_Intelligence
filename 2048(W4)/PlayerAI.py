# Artifical Intelligence @ edX
# Week4 Project
# Adversial Search and Games : 2048
# Renjie Li, rl2932@columbia.edu

from BaseAI import BaseAI
import time
import numpy


class PlayerAI(BaseAI):

    def getMove(self, grid):
        self.start_time = time.clock()  # To prevent timeout
        moves = grid.getAvailableMoves()
        best_move = 0 # What we need to return, at first I set it to None, but it may lead to some problems..
        MAX = -numpy.inf # The root is a MAX node, so we need to set the default MAX to -infinity

        self.smoothweight = 0.1
        self.monotoweight = 1.0
        self.emptyweight = 2.7
        self.maxweight = 1.0


        for step in moves:
            #if time.clock() - self.start_time >0.195:
            #    break
            child = grid.clone() # Deepcopy
            child.move(step)
            self.depth = 4
            self.alpha = -numpy.inf
            self.beta = numpy.inf
            score = self.Min(child)
            if score > MAX:
               MAX = score
               best_move = step
        return best_move

    def Min(self,grid):
        # Find the minimum evaluation(heuristic) for the computerAI
        if time.clock() - self.start_time > 0.04 or self.depth ==0 or grid.canMove()==False:
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

            if Min <= self.alpha:
                break

            if Min < self.beta:
                self.beta = Min

        return Min

    def Max(self,grid):
        # Find the maximum evaluation(heuristic) for the playerAI
        if time.clock() - self.start_time > 0.04 or self.depth==0  or grid.canMove()==False:
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

            if Max >= self.beta:
                break

            if Max > self.alpha:
                self.alpha = Max

        return Max




    def Heuristic(self,grid):
        if grid.canMove() == False:
            return -numpy.inf
        emptyCells = len(grid.getAvailableCells())
        maxTile = grid.getMaxTile()


        actual_score = 0
        for i in range(4):
            for j in range(4):
                actual_score+= grid.map[i][j]


        return emptyCells






