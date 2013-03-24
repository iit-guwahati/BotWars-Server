#!/usr/bin/python
# Author : Rajat Khanduja <rajatkhanduja13@gmail.com>

from BotWarsHandler import *
from SocketServer import ThreadingMixIn
import sys
import logging
import judge

def usage():
  print "Usage : python BotWarsServer.py <port_number>"

class MultiThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  pass


if __name__=='__main__':
  try:
    HOST_NAME   = '172.16.25.187'
    PORT_NUMBER = int(sys.argv[1])
  except Exception:
    usage()
    exit(0)
  
  httpd = MultiThreadedHTTPServer((HOST_NAME, PORT_NUMBER), BotwarsHandler)
  logging.basicConfig(filename="BotWars.log", level=logging.DEBUG,
                      format='%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s] :: %(message)s',
                      datefmt='%m/%d/%Y %H:%M:%S')
  logging.info("Server started on port %s", PORT_NUMBER)
  judge.init()
  logging.info("Compiled runner file")
  print "Server running. Use Ctrl+c to stop the server."
  try:
    httpd.serve_forever()
  except KeyboardInterrupt as key:
    print "Keyboard interrupt occured"

