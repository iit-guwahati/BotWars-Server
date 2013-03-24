#!/usr/bin/python
# Author : Rajat Khanduja
# 
# 1 : North/up
# 2 : NE
# 5 : E
# 8 : SE
# 7 : S
# 6 : SW
# 3 : W
# 0 : NW


import os
import logging

dictionary = "CSW12.txt"
TIME_LIM = 10
MEM_LIM  = 200000000
testFiles = [
            ('input_scramble100.txt', 'output_scramble.txt'),
            ('input_scramble.txt',  'output_scramble.txt'),
            ('input_scramble1.txt', 'output_scramble.txt'),
            ('input_scramble2.txt', 'output_scramble.txt'),
            ('input_scramble3.txt', 'output_scramble.txt')
            ]

MOVEMENTS = [1, 2 ,5 ,8 , 7 ,6, 3, 0]
SCORES = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4,
          8, 4, 10]

def setup(sourceFile, problemsDir):
  global dictionary
  dictionary = os.path.join(problemsDir, dictionary)

def evaluate(inputData, expectedOutput, producedOutput, sourceFile):
  
  words = set(map(lambda x: x.strip(), open(dictionary).readlines()))  
  foundWords = set(producedOutput.strip().split('\n'))  
  inputLines = map(lambda x: x.strip(), inputData.split('\n'))
  logging.debug("n = %s", inputLines[0])
  n = int(inputLines[0])
  tiles = inputLines[1:]
  scores = 0
  
  for foundWord in foundWords:
    try:
      startpos = map(lambda x: int(x), foundWord.split(' ')[0].split(','))
      movement = foundWord.split(' ')[1]
      seq = tiles[startpos[0]][startpos[1]]
      for x in movement:
        x = int(x)
        if x not in MOVEMENTS:
          raise IndexError('Illegal Movement')  # FIX THIS
        else:
          startpos[0] += x / 3 - 1
          startpos[1] += x % 3 - 1
          seq += tiles[startpos[0]][startpos[1]]
    except Exception as e:
      logging.debug(e)
      continue
    
    logging.debug("Observed sequence : %s %d", seq, len(words))
    if seq in words:
      scores += sum(map(lambda x: SCORES[ord(x) - ord('A')], seq))
    else: 
      continue

  return scores
