#!/usr/bin/env python

__author__ = "mathieu@garambrogne.net"

import roundrobin.rrd

class Graph(object):
	def __init__(self, image,
			end='now', step=None, start='end-7200s',
			width=1200, height=None,
			only_graph = False, full_size_mode = False,
			title=None, vertical_label="python's roundrobin"):
		#self.imgformat = 'PNG'
		self.image = image
		self.end = end
		self.step = step
		self.start = start
		self.width = width
		self.height = height
		self.title = title
		self.vertical_label = vertical_label
		self.only_graph = only_graph
		self.full_size_mode = full_size_mode
		self.datas = []
		self.graphs = []
	def data(self, data):
		self.datas.append(data)
	def graph(self, graph):
		self.graphs.append(graph)
	def draw(self):
		tmp = "{image} --lazy --start {start} --end {end}".format(
			image = self.image,
			start = self.start,
			end = self.end)
		if self.step != None:
			tmp += " --step %s" % self.step
		if self.only_graph:
			tmp += ' --only_graph'
		if self.title != None:
			tmp += ' --title "%s"' % self.title
		if self.vertical_label != None:
			tmp += ' --vertical-label "%s"' % self.vertical_label
		for data in self.datas:
			tmp += ' ' + data
		for graph in self.graphs:
			tmp += ' ' + graph
		#rrd_wrapper.debug = True
		#print 'graph %s ' %  tmp
		roundrobin.rrd.rrd_wrapper('graph %s' %  tmp)

#datas

def DEF(vname, rrd, ds_name, cf = 'AVERAGE'):
	return 'DEF:%s=%s:%s:%s' % (vname, rrd, ds_name, cf)

def CDEF():
	pass

def VDEF():
	pass

#graphs

def LINE(width, value, color = "0000FF", legend = None, stack = False):
	tmp = 'LINE%s:%s' % (width, value)
	if color != None:
		tmp += '#%s' % color
	if legend != None:
		tmp += ':%s' % legend
	if stack:
		tmp += ':STACK'
	return tmp