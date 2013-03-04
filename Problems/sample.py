#!/usr/bin/python
# Author : Rajat Khanduja
#
# Sample problem definition to show how to provide necessary information to the
# server. This file demonstrates how to give the functions and constants
# required by BotWarsHandler
#
# Required Constants
#   testFiles : array of (inputFile, outputFile)
#   MEM_LIM   : memory limit to be imposed on the running program
#   TIME_LIM  : time limit to be imposed on the running program
#
# Required functions

import filecmp

testFiles = [("input_sample.txt", "output_sample.txt")]
MEM_LIM   = 200000000 # bytes
TIME_LIM  = 5 # seconds

def setup():
  pass

def evaluate(inputData, expectedOutput, producedOutput):
  '''
  Function returns a real number (integer or float) as a score. Higher the score,
  better the performance.
  
  example :
  if expectedOutput == producedOutput:
    return 1
  else:
    return 0
  
  '''
  if expectedOutput == producedOutput:
    return 1
  else:
    return 0
