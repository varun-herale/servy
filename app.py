#!/usr/bin/python2

from flask import *
import logging
import logging.handlers
import datetime

app = Flask(__name__)
LOG_FILENAME = 'req.log'
info_log = logging.getLogger('req')
info_log.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1024 * 1024 * 100,
    backupCount=20
    )

info_log.addHandler(handler)

@app.route('/')
def hello_world():
    info_log.info('\t'.join([
            datetime.datetime.today().ctime(),
            request.remote_addr,
            request.method,
            request.url,
            request.data]))
    return render_template('index.html')
  
@app.route('/<path:url>')
def new_path(url):
    #info_log.info('\t'.join([request.remote_addr,request.url]))
    info_log.info('\t'.join([
            datetime.datetime.today().ctime(),
            request.remote_addr,
            request.method,
            request.url,
            request.data]))
    return render_template(url)

if __name__ == '__main__':
    app.run(debug=True)
