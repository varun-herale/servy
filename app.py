#!/usr/bin/python2

# All required imports
import os
import anydbm
import pickle
import logging
import logging.handlers
from datetime import *
from flask import *


# Initialising flask and log file
app = Flask(__name__)
LOG_FILENAME = 'req.log'
info_log = logging.getLogger('req')
info_log.setLevel(logging.INFO)

# Handler for log file
handler = logging.handlers.RotatingFileHandler(
  LOG_FILENAME,
  maxBytes=1024 * 1024 * 100,
  backupCount=20
  )
info_log.addHandler(handler)

# Some more initialisation
# db = anydbm.open("dbm","c")
num_in_log = 0
# int(db["num"])
fmt = '%a %b %d %H:%M:%S %Y'
time_difference = timedelta(minutes = 30)  

# Request Class
class REQUEST:
  host = "127.0.0.1"
  dt = "Wed Dec 19 23:59:20 2012"
  url = "www.google.com"
  
# List of all files in the server
files = []
os.chdir("templates")
for file in os.listdir("."):
  files.append(file)
os.chdir("..")

# Rendering '/'
@app.route('/', methods=['GET', 'POST'])
def index():
  parse_rewrite()
  log_write('/', request)
  return render_template('index.html')

# Rendering everything else available
@app.route('/<path:url>', methods=['GET', 'POST'])
def new_path(url):
  if url in files:
    log_write(url, request)	
    return render_template(url)
  if url + '.html' in files:
    log_write(url, request)
    f.close()	
    return render_template(url + '.html')
  abort(404)

# 404 Error
@app.errorhandler(404)
def page_not_found(error):
  return render_template('page_not_found.html'), 404

# Write into log files
def log_write(url, request):
  global num_in_log
  num_in_log = num_in_log + 1
  db = anydbm.open("dbm","c")
  db["num"] = str(num_in_log)
  info_log.info('\t'.join([
  request.remote_addr,
  datetime.today().ctime(),
  request.method,
  request.url,
  request.data,
  ', '.join([': '.join(x) for x in request.headers])]))
  f = open('log.txt', 'a')
  req = REQUEST()
  req.host = request.remote_addr
  req.dt = datetime.today().ctime()
  req.url = request.url
  pickle.dump(req, f)
  f.close()

def parse_rewrite():
  global num_in_log
  global fmt
  i = open('log.txt', 'r')
  o = open('temp_log.txt', 'w')
  temp_num_in_log = num_in_log
  num_in_log = 0
  req = REQUEST()
  while temp_num_in_log > 1:
    req = pickle.load(i)
    temp = datetime.strptime(req.dt, fmt)
    temp_now = datetime.strptime(datetime.today().ctime(), fmt)
    if (temp + time_difference) > temp_now:
      pickle.dump(req,o)
      num_in_log = num_in_log + 1
    temp_num_in_log = temp_num_in_log - 1
  o.close()
  i.close()
  os.remove("log.txt")
  os.rename("temp_log.txt", "log.txt")

if __name__ == '__main__':
  app.run(debug=True)
