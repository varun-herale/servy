#!/usr/bin/python2

from flask import *
import logging
import logging.handlers
import datetime
from datetime import *
import os
import anydbm
import pickle

app = Flask(__name__)
LOG_FILENAME = 'req.log'
info_log = logging.getLogger('req')
info_log.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
  LOG_FILENAME,
  maxBytes=1024 * 1024 * 100,
  backupCount=20
  )

db = anydbm.open("dbm","c")
num_in_log = int(db["num"])
fmt = '%a %b %d %H:%M:%S %Y'
time_difference = timedelta(minutes = 30)  
  
class REQUEST:
	host = "127.0.0.1"
	dt = "Wed Dec 19 23:59:20 2012"
	methd = "GET"
	url = "www.google.com"
	useragent = "Mozilla/5.0"
	
info_log.addHandler(handler)

files = []
os.chdir("templates")
for file in os.listdir("."):
    files.append(file)
os.chdir("..")

@app.route('/', methods=['GET', 'POST'])
def index():
  log_write('/', request)
  return render_template('index.html')
 
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

@app.errorhandler(404)
def page_not_found(error):
  return render_template('page_not_found.html'), 404
  
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
	req.methd = request.method
	req.url = request.url
	req.useragent = request.headers.get('User-Agent')
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
