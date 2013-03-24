#!/usr/bin/python
# Author : Rajat Khanduja
# 
# Problem description
# Print numbers from 1 to 1000 with on number on each line but if the number is
# a square, print "Dart"; if it's a cube, print "Part". If the number is both
# a square and a cube, print "DartPart" (on one line). This has to be done in
# the minimal characters (or keystrokes) of code. The final score is given by
# s = (300 - characters_of_code) / 3 . 
# If the number of characters >= 300, then the score is 1.

import filecmp

testFiles = [("input_dartpart.txt", "output_dartpart.txt")]
MEM_LIM   = 200000000 # bytes
TIME_LIM  = 1 #seconds

def setup(sourceFile, problemsDir):
  pass

def evaluate(inputData, expectedOutput, producedOutput, sourceFile):
  if expectedOutput == producedOutput:
    sourceCode = open(sourceFile).read() 
    if len(sourceCode) >= 300:
      return 1
    else:
      return (300 - len(sourceCode)) / 3
  else:
    return 0 
