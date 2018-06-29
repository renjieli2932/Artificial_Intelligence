'''
The purpose of this script is to test some basic functions in Python
'''

import Queue as Q
import time
import resource
import sys
import math
import sets
#sm = sys.argv[1].lower()
#begin_state = sys.argv[2].split(",")
#begin_state = tuple(map(int, begin_state))

a = tuple([1,2,3,4])
b = tuple([5,6,7,8])
q = Q.Queue()
q.put(1)
q.put(2)
q.put(3)
print(2 in q)
test= sets.Set()
test.add(a)
test.add(b)

