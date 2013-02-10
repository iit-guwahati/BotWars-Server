#!/usr/bin/python
import subprocess
import string

def init():
	compilec = ['/usr/bin/gcc', 'runner.c', '-o', 'runner','-lm']
	subprocess.call(compilec)
	
def com(filename,cerrfile,inputfile,outputfile,memlimit,timelimit):
	#print "Will compile " + filename
	#filename=raw_input("File name please\n")
	dotpos = filename.find(".")
	language=filename[dotpos+1:]
	if ( language == 'c' ):
		compilec = ['/usr/bin/gcc','-lm', filename]
		try:
			warnerr = open(cerrfile,'w')
			subprocess.call(compilec,stderr=warnerr)
			warnerr.close()
		except Exception as e:
			print e
			pass
			
			
	elif ( language == 'py' ):
		try:
			subprocess.call(['chmod','a+x',filename])
			runc = ['./runner', filename, '--input='+inputfile, '--output='+outputfile, '--mem='+memlimit, '--time='+timelimit]
			fo = open(cerrfile,'w')
			subprocess.call(runc,stderr=fo)
			fo.close()
		except Exception as e:
			print e
			pass
	
	
	
	elif ( language == 'cpp' ):
		compilecpp = ['/usr/bin/g++', filename]
		try:
			foo = open(cerrfile,'w')
			subprocess.call(compilecpp,stderr=foo)
			foo.close()
		except Exception as e:
			print e
			pass
	
	with open(cerrfile, 'r') as cerr_file:
    		cerr = cerr_file.read()
	return cerr
	
	
	
def run(filename,runerrfile,inputfile,outputfile,memlimit,timelimit):
	dotpos = filename.find(".")
	language=filename[dotpos+1:]
	fo = open(runerrfile,'w')

	if ( language == 'c' ):
		try:
			runc = ['./runner', 'a.out', '--input='+inputfile, '--output='+outputfile, '--mem='+memlimit, '--time='+timelimit]
			subprocess.call(runc,stderr=fo)
		except Exception as e:
			print e
			pass
	
	elif ( language == 'cpp' ):
		try:
			runcpp = ['./runner', 'a.out', '--input='+inputfile, '--output='+outputfile, '--mem='+memlimit, '--time='+timelimit]
			subprocess.call(runcpp)
		except Exception as e:
			print e
			pass
	elif (language == 'py'):
		return
			
	if(language == 'c' or language =='cpp'):
		with open(runerrfile, 'r') as error_file:
    			error = error_file.read()
		
	with open(outfile, 'r') as output_file:
		output = output_file.read()
	return error,output
		

init()
com("hello.py","cerrfile.txt","input.txt","output.txt","200000000","2.0")
run("hello.py","runerr.txt","input.txt","output.txt","200000000","2.0")
			

