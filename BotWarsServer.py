from BotWarsHandler import *
import sys
import logging

def usage():
  print "Usage : python BotWarsServer.py <port_number>"


if __name__=='__main__':
  try:
    HOST_NAME   = 'localhost'
    PORT_NUMBER = int(sys.argv[1])
  except Exception:
    usage()
    exit(0)
  
  httpd = HTTPServer((HOST_NAME, PORT_NUMBER), BotwarsHandler)
  logging.basicConfig(filename="BotWars.log", level=logging.DEBUG,
                      format='%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s] :: %(message)s',
                      datefmt='%m/%d/%Y %H:%M:%S')
  logging.info("Server started on port %s", PORT_NUMBER)
  print "Server running. Use Ctrl+c to stop the server."
  try:
    httpd.serve_forever()
  except KeyboardInterrupt as key:
    print "Keyboard interrupt occured"

