'''
The purpose of this script is to test some basic functions in Python
'''

import Queue as Q
import time
import resource
import sys
import math

sm = sys.argv[1].lower()
begin_state = sys.argv[2].split(",")
begin_state = tuple(map(int, begin_state))

for i, item in enumerate(begin_state):
    print(i,item)