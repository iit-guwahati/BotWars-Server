import time, json, urlparse, os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from base64 import b64decode
import logging

TEMP_DIR = "/tmp/BOTWARS_TMP"  
class BotwarsHandler (BaseHTTPRequestHandler):
#  self._evaluator
  def do_HEAD(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    
  def do_POST(self):
    ''' Respond to POST request.'''
    # Extract and print the contents of the POST
    logging.debug('Received post request')
    recvTime  = int(time.time())
    self.do_HEAD()
    length    = int(self.headers['Content-Length'])
    post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
    teamname  = post_data['teamname'][0]
    teampass  = post_data['teampassword'][0]
    problemNo = post_data['problemnumber'][0]
    filename  = post_data['filename'][0]
    filedata  = b64decode(post_data['filedata'][0])
    logging.debug('Post request details :\t' + 
                  'teamname  = %s ;;' + 
                  'teampass  = %s ;;' +
                  'problemNo = %s ;;' + 
                  'filename  = %s ;;', teamname, teampass, problemNo, filename)

    # TODO : Add authentication part

    # Check if the folder for the user exists
    folder = os.path.join(TEMP_DIR, teamname, problemNo)
    if not os.path.exists(folder):
      os.makedirs(folder)
    # Create filename using the folder information
    filename = os.path.join(folder, filename)
    # Dump data into file
    self.dumpFile(filename, filedata)
    # TODO : Call evaluation methods

    # Rename file so as to be able to keep older versions.
    os.rename(filename, filename + str(recvTime))
  
    # TODO : Return evaluation results
    self.wfile.write("File saved")
    return 

  def do_GET(self):
  # Handle this as error.
    pass

  def dumpFile(self, filename, filedata):
    fp = open (filename,'w')
    fp.write(filedata)
    fp.close()


