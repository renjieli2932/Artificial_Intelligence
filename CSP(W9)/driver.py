# Artifical Intelligence @ edX
# Week9 Project CSP
# Renjie Li, rl2932@columbia.edu

import sys
import Queue as Q

class sudoku(object):

    def __init__(self):
        self.start_state = sys.argv[1] # Start state of the board
        if len(self.start_state) != 81: # Prevent input error, which frequently happens during debugging...
            raise ValueError("Invalid Initial State")
        for i in range(81):
            print(self.start_state[i]+" "),
            if (i+1) % 9 ==0:
                print (' ')

        self.rows = 'ABCDEFGHI'
        self.columns = '123456789'
        self.variables = self.get_variables() # [A1,A2.....I8,I9]
        self.domain = '123456789' # [1,2,...,9]
        self.layout = self.get_dictionary() # Dictionary
        self.neighbors = self.get_neighbors()  # Get neighbors , it's a dictionary, neightbors['A1'] will return a set that contains all the neighbors of A1
        self.constraints  = self.get_constraints() # Get constraints
        if self.AC3() and self.isSolved():
            self.output('AC3')
        else:
            self.layout = self.get_dictionary()  # Re-initialization
            self.layout = self.BTS()
            self.output('BTS')



    def combine(self,item1,item2):
        list = []
        for i in item1:
            for j in item2:
                list.append(i+j)
        return list

    def get_variables(self):
        '''
        To create a list that contains every cell of the board (A1 to I9)
        :return: ['A1','A2'....'I9']
        '''
        return self.combine(self.rows,self.columns)


    def get_dictionary(self):
        # To create a dictionary
        index = 0
        dictionary = dict() # Initialization
        for item in self.variables:
            if self.start_state[index] != '0':
                dictionary[item] = self.start_state[index]
            else:
                dictionary[item] = self.domain
            index += 1
        return dictionary

    def get_neighbors(self):
        list = []
        for i in self.columns:
            list.append(self.combine(self.rows,i))
        for i in self.rows:
            list.append(self.combine(i,self.columns))
        for i in ('ABC','DEF','GHI'):
            for j in ('123','456','789'):
                list.append(self.combine(i,j))
        # Each sub-list in the list should be 1 of the 27 constraints in lecture nots
        # which need to be all different (1 to 9)
        neighbors = dict()
        for item in self.variables:
            its_neighbor = []
            for i in list:
                if item in i:
                    its_neighbor = set.union(set(its_neighbor), set(i))
            its_neighbor.remove(item)
            neighbors[item] = its_neighbor

        return neighbors

    def get_constraints(self):
        constraints = set()
        for i in self.variables:
            for j in self.neighbors[i]:
                constraints.add((i,j))
        return constraints



    def AC3(self):
        Frontier = Q.Queue() # A queue of arcs

        for arc in self.constraints:
            Frontier.put(arc) # Initialization

        while not Frontier.empty():
            Xi,Xj = Frontier.get() # Remove-first queue

            if self.Revise(Xi,Xj):
                if len(self.layout[Xi]) == 0:
                    return False
                for Xk in self.neighbors[Xi]:
                    Frontier.put((Xk,Xi))

        return True

    def Revise(self,Xi,Xj):
        revised = False

        for x in self.layout[Xi]:
            consistency = False

            for y in self.layout[Xj]:
                if Xj in self.neighbors[Xi] and y!=x:
                    consistency = True
                    break

            if not consistency:
                self.layout[Xi] = self.layout[Xi].replace(x,'')
                revised = True

        return revised


    def isSolved(self):
        for i in self.variables:
            if len(self.layout[i]) != 1:
                return False
        else:
            return True


    def BTS(self):
        return self.Backtrack({})


    def Backtrack(self,assignment):
        if self.isComplete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.layout[var]:
            if self.isConsistent(var,value,assignment):
                assignment[var] = value
                inferences = dict()
                inferences = self.Inference(var,value,assignment,inferences)
                if inferences != 'failure':
                    result = self.Backtrack(assignment)
                    if result != 'failure':
                        return result
                del assignment[var]
                self.layout = self.get_dictionary()  # Re-initialization
        return 'failure'

    def isComplete(self,assignment):
        if set(assignment.keys()) == set(self.variables): # The order in assignment might be random. We need to convert'em to set to compare
            return True
        return False

    def select_unassigned_variable(self,assignment):
        list = dict()
        for i in self.layout:
            if i not in assignment.keys():
                list[i] = len(self.layout[i])
        return min(list)


    def isConsistent(self,var,value,assignment):
        for i in self.neighbors[var]:
            if i in assignment.keys() and assignment[i] == value:
                return False
        return True

    def Inference(self,var,value,assignment,inferences):

        inferences[var] = value
        for i in self.neighbors[var]:
            if i not in assignment.keys() and value in self.layout[i]:
                if len(self.layout[i]) == 1:
                    return 'failure'

                self.layout[i] = self.layout[i].replace(value,'')
                if len(self.layout[i]) ==1:
                    if self.Inference(i,self.layout[i],assignment,inferences) == 'failure':
                        return 'failure'
        return inferences

    def output(self,method):
        output = ''
        for i in self.variables:
            output += self.layout[i]
        print(output+' '+method)
        output_name = 'output.txt'
        with open(output_name,'w') as f:
            f.write(output+' '+method)
        for i in range(81):
            print(output[i]+" "),
            if (i+1) % 9 ==0:
                print (' ')





if __name__ == "__main__":
    solver = sudoku()
