from BotWarsHandler import *
import sys



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
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  print "Server running. Use Ctrl+c to stop the server."
  try:
    httpd.serve_forever()
  except KeyboardInterrupt as key:
    print "Keyboard interrupt occured"

