#!/usr/bin/python
# Author : Rahul Huilgol <rahulrhuilgol@gmail.com>
# 
# This file defines functions required to compile and run the code and evaluate
# the output
# Currently supports only the following langauges
#  - C
#  - C++
#  - Python
#
# TODO : Take care of naming when multiple users might be accessing.

import subprocess
import logging
import os, sys, time
import codecs

PROBLEMS_DIR = "Problems"

class NoSuchProblemException(Exception):
  def __init__ (self, value):
    self.value = value

  def __str__ (self):
    return repr(self.value)

class CompilationError (Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

def judge(problemRef, sourceFile):
  '''
  This function takes as input the reference number of the problem
  and the submitted file and calls the compile-run function 
  appropriately. Eventually, it returns the score earned by the 
  submitted solution based on the problemRef and the evaluation
  function given in the file problems/problemRef.py
  '''

  # First ensure that the problem reference is a valid one.
  importFile = PROBLEMS_DIR + "." + str(problemRef)
  try:
    prob = __import__(importFile, fromlist = [problemRef])
  except Exception as e:
    logging.debug(str(e))
    raise NoSuchProblemException("Problem " + str(problemRef) + " not defined")
    return
  
  # Initial setup
  prob.setup()

  score = 0
  allErrors = ""
  # For each input, output pair run the test.
  # TODO : This step calls the compilation of files over and over. Fix this.
  try:
    for (inFile,outFile) in prob.testFiles:
      inFile  = os.path.join(PROBLEMS_DIR, inFile)
      outFile = os.path.join(PROBLEMS_DIR, outFile)
      (producedOutput, error) = compilerun(sourceFile, inFile, prob.MEM_LIM,
                                           prob.TIME_LIM)
      inputData = open(inFile).read()
      expectedOutput = open(outFile).read()
      if not error:
        score += prob.evaluate (inputData, expectedOutput, producedOutput)
      else:
        allErrors += error + "\n"
  except CompilationError as e:
    logging.debug ("CompilationError:" + str(e))
    allErrors += str(e)
    pass
  except Exception as e:
    logging.info (str(e))
    pass
    
    
  return score, allErrors


def init():
  '''
  Initializations required for judging steps.
  '''
  compilec = ['/usr/bin/gcc', 'runner.c', '-o', 'runner','-lm']
  subprocess.call(compilec)

def compilerun(filename, inputfile, memlimit, timelimit):
  TEST_DIR    = os.path.dirname(filename)
  outFiles    = {'c'  : filename + ".out",
                 'cpp': filename + '.out'}
  compiler    = {'c'  : ['/usr/bin/gcc', '-lm', '-w', '-o', outFiles['c']],
                 'cpp': ['/usr/bin/g++', '-lm', '-w', '-o', outFiles['cpp']]}
  interpreter = {'py' : '/usr/bin/python'}              
    # Convert all parameters to string
  filename   = str(filename)
  inputfile  = str(inputfile)
  memlimit   = str(memlimit)
  timelimit  = str(timelimit)
  logging.debug("%s; %s; %s; %s", filename, inputfile, memlimit, timelimit)
  
  # Find language of the program
  dotpos = filename.find(".")
  language = filename[dotpos + 1:]
  logging.debug("Language of file %s is '%s'", filename, language)

  compileerror = False
  
  # Create and open output and error files
  t = str(int(time.time()))
  errfile    = os.path.join(TEST_DIR, os.path.basename(inputfile) + "_err_" + t)
  outputfile = os.path.join(TEST_DIR, os.path.basename(inputfile) + "_out_" + t)
  ferr = open(errfile,'w')
  fout = open(outputfile, 'w') # Ensures that the file is created
  fout.close()  # Close it as only creation of file is required
  logging.debug("Created output file : %s ; Created error file : %s", errfile, outputfile)
  error  = ""
  output = ""
  # Check if it is a compiled language
  if language in compiler:
    compiler[language].append(filename)
    subprocess.call(compiler[language], stderr = ferr)
    with codecs.open(errfile, encoding='utf-8') as error_file:
      error = error_file.read()
    if not error:
      logging.debug("Compiled %s successfully", filename)
      run =  ['./runner', outFiles[language], '--input=' + inputfile, 
              '--output=' + outputfile, '--mem=' + memlimit, 
              '--time=' + timelimit]
      subprocess.call(run, stderr = ferr)
    else:
      logging.debug("Error when compiling %s", filename)
      compileerror = True
      raise CompilationError(error)
  elif language in interpreter:
    run = ['./runner', interpreter[language], filename, '--input=' + inputfile, 
           '--output=' + outputfile, '--mem=' + memlimit, 
           '--time=' + timelimit]
    subprocess.call(run, stderr = ferr)
    with open(errfile, 'r') as error_file:
      error = error_file.read()
    if error:
      compileerror = True       
      
  ferr.close()
  with open(errfile, 'r') as error_file:
    if compileerror == False:
      error = error_file.read()
    else:
      error = 'CERR  ' + error_file.read()
#        print error
  with open(outputfile, 'r') as output_file:
    output = output_file.read()
#   print output
  
    # TODO : Delete error and output files
  return (output, error)
