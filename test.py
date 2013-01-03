#!/usr/bin/python2

# All required imports
import os
import pickle
import logging
import logging.handlers
from datetime import *
from flask import *

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

# Display
def disp_lay(main_node, level):
	for c in main_node.children:
		print c.url
		disp_lay(c, level+1)
	if level == 1:
		print 'End of branch'

# Read Tree
def make_tree():
	i = open('tree_struct.txt', 'r')
	main_node = Node('base', 0)
	main_node = pickle.load(i)
	disp_lay(main_node, 0)

if __name__ == '__main__':
	make_tree()
