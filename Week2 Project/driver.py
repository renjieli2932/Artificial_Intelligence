# Artifical Intelligence @ edX
# Week2 Project
# Renjie Li, rl2932@columbia.edu
import Queue as Q
import time
import resource
import sys
import math
import sets # imported by myself

## The Class that Represents the Puzzle

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []

        for i, item in enumerate(self.config): # to figure out the position of the empty space
            if item == 0:
                self.blank_row = i / self.n
                self.blank_col = i % self.n
                break

    def display(self): # display the current configuration
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print line

    def move_left(self):
        if self.blank_col == 0:  # If the empty space is in the first column, no left move allowed
            return None    
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1   # the element on the left of the empty space
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index] # swap 
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""
        # add child nodes in order of UDLR
        if len(self.children) == 0: 
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)

        return self.children


class PriorityQueue(object):

    def __init__(self):
        self.Queue = []
        self.Distance = []

    def put(self,state):
        self.Queue.append(state)
        self.Manhattan()

    def Manhattan(self):
        gn = self.Queue[-1].cost # cost to reach node n
        current_state = self.Queue[-1].config
        size = self.Queue[-1].n # size of the puzzle
        hn = 0 # heuristic cost from n to goal
        for i,num in enumerate(current_state): # i: real position, num: desired position
            if num != 0:
                hn += abs(i//size - num//size) + abs(i%size - num%size)
        fn = gn+hn
        self.Distance.append(fn)

    def empty(self):
        if self.Queue == []:
            return True
        else:
            return False

    def deleteMin(self):
        index = self.Distance.index(min(self.Distance)) # Find out the index of the minimum fn
        state = self.Queue.pop(index)
        self.Distance.pop(index)
        return state


def bfs_search(initial_state):
    starttime = time.time()
    Frontier = Q.Queue() # create a new queue as frontier
    Frontier.put(initial_state) # initialization
    Stored = sets.Set()          # Since we can not use 'in' to queue (to check if the element is in frontier), create a set to store all the elements in Frontier
    Stored.add(initial_state.config)
    Explored = sets.Set()        # Used to store the nodes that we have explored
    Expansion = 0
    Max_Search_Depth = 1
    while not Frontier.empty():
        state = Frontier.get()
        Explored.add(state.config)
        if test_goal(state.config):
            endtime = time.time()
            running_time = endtime - starttime
            path = find_path(state)
            output(state.cost,Expansion,path,Max_Search_Depth,running_time)
            return
        else:
            state.expand()
            Expansion +=1
            for child in state.children:
                if (child.config not in Stored) and (child.config not in Explored):
                    Frontier.put(child)
                    Stored.add(child.config)
                    if child.cost > Max_Search_Depth:
                        Max_Search_Depth = child.cost



def dfs_search(initial_state):
    starttime = time.time()
    Frontier = []# create a new queue as frontier
    Frontier.append(initial_state) # initialization
    Stored = sets.Set()          # Since we can not use 'in' to queue (to check if the element is in frontier), create a set to store all the elements in Frontier
    Stored.add(initial_state.config)
    Explored = sets.Set()        # Used to store the nodes that we have explored
    Expansion = 0
    Max_Search_Depth = 1
    while Frontier != []:
        state = Frontier.pop()
        Explored.add(state.config)
        if test_goal(state.config):
            endtime = time.time()
            running_time = endtime - starttime
            path = find_path(state)
            output(state.cost,Expansion,path,Max_Search_Depth,running_time)
            return
        else:
            state.expand()
            state.children = state.children[::-1] # Push onto the stack in reverse-UDLR order;
            Expansion +=1
            for child in state.children:
                if (child.config not in Stored) and (child.config not in Explored):
                    Frontier.append(child)
                    Stored.add(child.config)
                    if child.cost > Max_Search_Depth:
                        Max_Search_Depth = child.cost


def A_star_search(initial_state):
    starttime = time.time()
    Frontier = PriorityQueue()
    Frontier.put(initial_state) # Initialization
    Stored = sets.Set()          # Since we can not use 'in' to queue (to check if the element is in frontier), create a set to store all the elements in Frontier
    Stored.add(initial_state.config)
    Explored = sets.Set()        # Used to store the nodes that we have explored
    Expansion = 0
    Max_Search_Depth = 1
    while not Frontier.empty():
        state = Frontier.deleteMin()
        Explored.add(state.config)
        if test_goal(state.config):
            endtime = time.time()
            running_time = endtime - starttime
            path = find_path(state)
            output(state.cost, Expansion, path, Max_Search_Depth, running_time)
            return
        else:
            state.expand()
            Expansion += 1
            for child in state.children:
                if (child.config not in Stored) and (child.config not in Explored):
                    Frontier.put(child)
                    Stored.add(child.config)
                    if child.cost > Max_Search_Depth:
                        Max_Search_Depth = child.cost


def test_goal(puzzle_state):

    """test the state is the goal state or not"""
    goal_state = tuple([0,1,2,3,4,5,6,7,8])
    return puzzle_state == goal_state

def find_path(state):
    path = []
    while state.parent is not None:
        path.insert(0,state.action)
        state = state.parent
    return path

def output(cost,expansion,path,max_depth,runtime):
    print('path_to_goal',path)
    print("cost_of_path", cost)
    print("nodes_expanded", expansion)
    print("search_depth", cost)
    print("max_search_depth", max_depth)
    print("running_time", runtime)
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0  # in Megabytes
    print("max_ram_usage", usage)  # Looks weird comparing to the reference results, maybe because I am using Mac?

    with open('output.txt','w') as f:
        f.write('path_to_goal:'+str(path)+'\n')
        f.write('cost_of_path:'+str(cost)+'\n')
        f.write('nodes_expanded:'+str(expansion)+'\n')
        f.write('search_depth:'+str(cost)+'\n')
        f.write('max_search_depth:'+str(max_depth)+'\n')
        f.write('running_time:'+str(runtime) +'\n')
        f.write('max_ram_usage:'+str(usage)+'\n')

def main():
    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":
        bfs_search(hard_state)
    elif sm == "dfs":
        dfs_search(hard_state)
    elif sm == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

if __name__ == '__main__':
    main()