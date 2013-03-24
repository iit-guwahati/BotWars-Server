#!/usr/bin/python
#
# This file is part of the BotWarsServer program.
# Copyright (C) 2013 Rajat Khanduja, Suhail Sherif
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The program starts execution in this file.

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
    HOST_NAME   = '0.0.0.0'
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

