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
# This file contains the functions required to handle the incoming requests.


import time, json, urlparse, os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from base64 import b64decode
import logging
from judge import judge, NoSuchProblemException
import BotWarsDb as db

TEMP_DIR = "/tmp/BOTWARS_TMP"  

# Return strings
INVALID_PROBLEM  = "Invalid Problem number"
INVALID_AUTHENTICATION  = "Invalid Authentication. Please check your username and password again."
FILEDATA_MISSING = "Error receiving file content. Please check if you are choosing the correct file." 

class BotwarsHandler (BaseHTTPRequestHandler):
#  self._evaluator
  def do_HEAD(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    
  def do_POST(self):
    ''' Respond to POST request.'''
    # Extract and print the contents of the POST
    logging.debug('Received post request at '+self.path)

    recvTime  = int(time.time())
    length    = int(self.headers['Content-Length'])
    post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
    teamname  = post_data['teamname'][0]
    teampass  = post_data['teampassword'][0]

    if self.path=='/submit':

      problemNo = post_data['problemnumber'][0]
      filename  = post_data['filename'][0]

      try:
        filedata  = b64decode(post_data['filedata'][0])
      except Exception as e:
        logging.info ('Caught exception %s', e)
        self.do_HEAD()
        self.wfile.write(FILEDATA_MISSING)
        return

      logging.debug('Post request details :\t' + 
                  'teamname  = %s ;;' + 
                  'teampass  = %s ;;' +
                  'problemNo = %s ;;' + 
                  'filename  = %s ;;', teamname, teampass, problemNo, filename)

      if not db.authenticate(teamname, teampass):
        self.do_HEAD()
        self.wfile.write(INVALID_AUTHENTICATION)
        return

      # Check if the folder for the user exists
      folder = os.path.join(TEMP_DIR, teamname, problemNo)
      if not os.path.exists(folder):
        os.makedirs(folder)
      # Create filename using the folder information
      filename = os.path.join(folder, filename)

      # Dump data into file
      self.dumpFile(filename, filedata)

      score = 0
      # Judge solution
      try:
        score, errors = judge (problemNo, filename)
      except NoSuchProblemException as e:
        self.do_HEAD()
        self.wfile.write(INVALID_PROBLEM)
        logging.debug(str(e))
        return      
    
      # Rename file so as to be able to keep older versions.
      newfilename = filename + str(recvTime)
      os.rename(filename, newfilename)
  
      db.updateSubmissions(teamname, problemNo, recvTime, newfilename, score, errors)

      # Return evaluation results
      self.do_HEAD()
      self.wfile.write("Score earned for solution : " + str(score))
      if errors:
        self.wfile.write("\nErrors\n" + errors)
      return

    elif self.path == '/leaderboard':
      self.do_HEAD()
      leaderboard = db.getLeaderboard()
      self.wfile.write(leaderboard)
      return

    elif self.path == '/score':
      if not db.authenticate(teamname, teampass):
        self.do_HEAD()
        self.wfile.write(INVALID_AUTHENTICATION)
        return

      self.do_HEAD()
      scores = db.getScores(teamname)
      self.wfile.write(scores)

  def do_GET(self):
    logging.debug('Received get request at '+self.path)
    self.do_HEAD()
    leaderboard = db.getLeaderboard().replace("\n", "<BR />").replace("\t", "    ")
    self.wfile.write(leaderboard)
    return

  def dumpFile(self, filename, filedata):
    fp = open (filename,'w')
    fp.write(filedata)
    fp.close()
