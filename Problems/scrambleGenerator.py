#!/usr/bin/python
# Author : Rajat Khanduja
# Script to generate scramble tiles

import random
import sys
import bisect  

frequency = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1]

cumFreq = [sum(item for item in frequency[0:rank+1]) for rank in xrange(len(frequency))]

def randomString(length):
  return ''.join( chr(ord('A') + (bisect.bisect_left(cumFreq, random.randint(1, cumFreq[-1])))) for x in range(length))
    

n = int(sys.argv[1])
print n

for i in xrange(n):
  print randomString(n) 
