# Concept test

import numpy
import time
digits =  cols = "123456789"
rows = "ABCDEFGHI"


#FINDING THE CROSS PRODUCT OF TWO SETS
def cross(A, B):
	return [a + b for a in A for b in B]

squares = cross(rows, cols)

variables = squares
unitlist = ([cross(rows, c) for c in cols] +
            			 [cross(r, cols) for r in rows] +
            			 [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

start = time.time()
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)
end = time.time()
acr = end-start
constraints = {(variable, peer) for variable in variables for peer in peers[variable]}
#print(units['I6'])
#print(peers['A1'])
print(len(constraints))
#print(acr)