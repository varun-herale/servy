#!/usr/bin/python2

# All required imports
import os
import pickle
import logging
import logging.handlers
from datetime import *
from flask import *

# Some more initialisation
fmt = '%a %b %d %H:%M:%S %Y'
time_difference = timedelta(minutes = 30)  

# Request Class
class REQUEST:
	host = "127.0.0.1"
	dt = "Wed Dec 19 23:59:20 2012"
	url = "www.google.com"

# Tree Node Class
class Node(object):
	url = '127.0.0.1'
	data = 0
	children = []

	def __init__(self, url, data):
		self.url = url
		self.data = data
		self.children = []

	def add_child(self, obj):
		self.children.append(obj)

main_node = Node('base', 0)

# Make unfinished.txt
def make_unfinished():
	try:
		with open('log.txt') as f: pass
	except IOError as e:
		return 0
	os.rename('log.txt','temp_log.txt')
	i = open('temp_log.txt', 'r')
	o = open('unfinished_sessions.txt', 'a')
	req = REQUEST()
	while True:
		try:
			req = pickle.load(i)
		except EOFError:
			break
		else:
			pickle.dump(req,o)
	i.close()
	o.close()
	return 1

# Check if session is finished
def is_finished(current_host, time_now, time_prev, i):
	global fmt
	req= REQUEST()
	while True:
		try:
			req = pickle.load(i)
		except EOFError:
			if (time_now - time_prev) > time_difference:
				return 1
			else:
				return 0
		else:
			if str(req.host) != str(current_host):
				break
			else:
				temp_time = datetime.strptime(req.dt, fmt)
				if (temp_time - time_prev) > time_difference:
					return 1
				else:
					time_prev = temp_time

# Insert into tree for current session
def insert_to_tree(temp_node, req):
	flag = 0
	for c in temp_node.children:
		if c.url == req.url:
			c.data = c.data + 1
			flag = 1
		else:
			c = insert_to_tree(c, req)
	if (flag == 0) and ((temp_node.children == []) or (temp_node.url == "base")):
		new_node = Node(req.url, 1)
		temp_node.add_child(new_node)
	return temp_node

# Insert into main tree
def add_to_main(temp_node, main_node):
	for c in temp_node.children:
		flag = 0
		for d in main_node.children:
			if d.url == c.url:
				d.data = d.data + c.data
				d = add_to_main(c, d)
				flag = 1
		if flag == 0:
			main_node.add_child(c)
	return main_node

# Add session to tree
def add_to_tree(current_host, time_now, time_prev):
	global fmt
	global main_node
	i = open('unfinished_sessions.txt', 'r')
	o = open('temp_log.txt', 'w')
	req= REQUEST()
	temp_node = Node('base', 0)
	while True:
		try:
			req = pickle.load(i)
		except EOFError:
			main_node = add_to_main(temp_node, main_node)
			o.close();
			i.close();
			os.remove('unfinished_sessions.txt')
			os.rename('temp_log.txt', 'unfinished_sessions.txt')
			break
		else:
			if req.host != current_host:
				pickle.dump(req, o)
			else:
				temp_time = datetime.strptime(req.dt, fmt)
				if (temp_time - time_prev) > time_difference:
					main_node = add_to_main(temp_node, main_node)
					pickle.dump(req, o)
					while True:
						try:
							req = pickle.load(i)
						except EOFError:
							o.close()
							i.close()
							os.remove('unfinished_sessions.txt')
							os.rename('temp_log.txt', 'unfinished_sessions.txt')
							return None
						else:
							pickle.dump(req, o)
				else:
					time_prev = temp_time
					temp_node = insert_to_tree(temp_node, req)

# Display
#def disp_lay(main_node):
#	for c in main_node.children:
#		print c.url
#		disp_lay(c)
#	if main_node.children == []:
#		print "Empty"
#	else:  
#		print "End of branch \n"

# Make tree
def make_tree():
	global fmt
	global main_node
	if make_unfinished() == 0:
		make_tree()
	unfinished_sessions = []
	time_now = datetime.strptime(datetime.today().ctime(), fmt)
	i = open('unfinished_sessions.txt', 'r')
	req= REQUEST()
	while True:
		try:
			req = pickle.load(i)
		except EOFError:
			i.close()
			o = open('tree_struct.txt', 'w')
			pickle.dump(main_node, o)
			o.close()
			return None
			#make_tree()
		else:
			if req.host in unfinished_sessions:
				break
			time_prev = datetime.strptime(req.dt, fmt)
			if is_finished(req.host, time_now, time_prev, i) == 1:
				i.close()
				add_to_tree(req.host, time_now, time_prev)
				i = open('unfinished_sessions.txt')
			else:
				unfinished_sessions.append(req.host);

if __name__ == '__main__':
	make_tree()