#!/usr/bin/env python

__author__ = "mathieu@garambrogne.net"
__version__ = "0.1"

"""
Simple RRD wrapping for fetching data, when pyrrd is not enough
"""

from datetime import datetime
import os
import time

from result import Result, none_filter

try:
	import pexpect
	class RRDwrapper(object):
		def __init__(self):
			#LC_NUMERIC=en_US 
			self.debug = True
			self.spawn = pexpect.spawn('rrdtool -')
		def __call__(self, data):
			self.spawn.sendline(data)
			prems = True
			while True:
				self.spawn.expect('\r\n')
				if self.debug:
					print "[%s]" % self.spawn.before
				if prems:
					prems = False
					continue
				line = self.spawn.before
				if line[:3] == 'OK ':
					return
				if line[:7] == 'ERROR: ':
					raise Exception('rrd', line)
				yield line
	rrd_wrapper = RRDwrapper()
except ImportError:
	from subprocess import Popen, PIPE
	import os
	def rrd_wrapper(command):
		env = os.environ
		env['LC_NUMERIC'] = 'en_US'
		return Popen('rrdtool %s ' % command, env= env, shell=True, stdout=PIPE).stdout

def dateOrInt(date):
	"None became now, date or int can be used"
	if date == None:
		return int(time.time())
	if type(date) == datetime:
		return int(time.mktime(date.timetuple()))
	return date

def create(path, *datas, **dico):
	"Create a new RRD"
	cmd = ""
	if 'start' in dico:
		cmd += "--start %i " % dateOrInt(dico['start'])
	if 'step' in dico:
		cmd += "--step %i " % dateOrInt(dico['step'])
	if 'no_overwrite' in dico:
		cmd += "--no-overwrite "
	for data in datas:
		cmd += " %s" % str(data)
	rrd = RRD(path)
	rrd._create(cmd)
	return rrd

class DS(object):
	def __init__(self, name, dst, heartbeat, min_, max_):
		self.name = name
		self.dst = dst
		self.heartbeat = heartbeat
		self.min = min_
		self.max = max_
	def __repr__(self):
		return "DS:%s:%s:%i:%s:%s" % (self.name, self.dst, self.heartbeat, self.min, self.max)

class GAUGE(DS):
	def __init__(self, name, heartbeat, min_, max_):
		DS.__init__(self, name, 'GAUGE', heartbeat, min_, max_)

class COUNTER(DS):
	def __init__(self, name, heartbeat, min_, max_):
		DS.__init__(self, name, 'COUNTER', heartbeat, min_, max_)

class DERIVE(DS):
	def __init__(self, name, heartbeat, min_, max_):
		DS.__init__(self, name, 'DERIVE', heartbeat, min_, max_)

class ABSOLUTE(DS):
	def __init__(self, name, heartbeat, min_, max_):
		DS.__init__(self, name, 'ABSOLUTE', heartbeat, min_, max_)

class COMPUTE(object):
	def __init__(self, name, rpn):
		self.name = name
		self.rpn = rpn
	def __repr__(self):
		return "DS:%s:COMPUTE:%s" % (self.name, self.rpn)

class RRA(object):
	def __init__(self, cf, xff, steps, rows):
		self.cf = cf
		self.xff = xff
		self.steps = steps
		self.rows = rows
	def __repr__(self):
		return "RRA:%s:%s:%s:%s" % (self.cf, self.xff, self.steps, self.rows)

class AVERAGE(RRA):
	def __init__(self, xff, steps, rows):
		RRA.__init__(self, 'AVERAGE', xff, steps, rows)

class MIN(RRA):
	def __init__(self, xff, steps, rows):
		RRA.__init__(self, 'MIN', xff, steps, rows)

class MAX(RRA):
	def __init__(self, xff, steps, rows):
		RRA.__init__(self, 'MAX', xff, steps, rows)

class LAST(RRA):
	def __init__(self, xff, steps, rows):
		RRA.__init__(self, 'LAST', xff, steps, rows)

class RRD(object):
	"Round robin database"
	def __init__(self, path):
		self.path = path
		self.folder, self.name = os.path.split(path)
	def __repr__(self):
		return "<RRD %s>" % self.path
	def _query(self, command, column=None, filter=none_filter):
		#return Result(Popen('rrdtool fetch %s %s ' % (self.path, command), env= env, shell=True, stdout=PIPE).stdout, column, filter)
		return Result(rrd_wrapper('fetch %s %s' % (self.path, command)), column, filter)
	def cmd(self, cmd, args=''):
		"pure rrdtool commands"
		#print '%s %s %s' % (cmd, self.path, args)
		return rrd_wrapper('%s %s %s' % (cmd, self.path, args))
	def blindCmd(self, cmd, args=''):
		"command without output"
		for l in self.cmd(cmd, args):
			pass
	def _create(self, args):
		"pure create"
		return self.blindCmd('create', args)
	def _update(self, args):
		"pure update"
		return self.blindCmd('update', args)
	def updateOnce(self, date, value):
		self.update([(date, value)])
	def update(self, datas):
		"""
		datas is an iterable list of date, value tuples
		RRD.update is faster than iteration with RRD.updateOnce
		[FIXME] flush for large list of data
		"""
		values = ''
		for date, value in datas:
			date = dateOrInt(date)
			values += '%s:%s ' % (date, value)
		self._update(values)
	def _info(self):
		return self.cmd('info')
	def fetch(self, *args, **dico):
		"""
r = RRD('toto.rrd')
for ts, value in r.fetch('AVERAGE', resolution=5, start='-5m'):
	print ts, value
"""
		return Query(**dico)(self)
	def info(self):
		info = {
			'ds'  :{},
			'rra' :{}}
		for line in self._info():
			#print line
			k,v = line[:-1].split(' = ')
			if k[:3] == 'ds[':
				d,vv = k.split('.',1)
				kk = d[3:-1]
				if not info['ds'].has_key(kk):
					info['ds'][kk] = {}
				info['ds'][kk][vv] = v
			else:
				if k[:4] == 'rra[':
					r,vv = k.split('.',1)
					info['rra'][int(r[4:-1])] = vv
				else:
					info[k] = v
		return info

if __name__ == '__main__':
	import time
	import os
	def query():
		for domain in os.listdir('collectd/rrd/') :
			print domain
			r = RRD('collectd/rrd/%s/load/load.rrd' % domain)
			query = AVERAGE(resolution=10, start='-10m', column=0, filter = lambda data: (1 - data))
			for ts, value in query(r):
				print ts, value
			print "----------------"
			for ts, value in r.fetch('AVERAGE', resolution=5, start='-5m'):
				print ts, value
			print "----------------"
			print list(query(r))[-3]
	def pipe():
		pipe = RRDwrapper()
		for domain in os.listdir('collectd/rrd/') :
			print datetime.fromtimestamp(int(list(pipe('last collectd/rrd/%s/load/load.rrd' % domain))[0]))
			print list(pipe('info collectd/rrd/%s/load/load.rrd' % domain))
	def info():
		for domain in os.listdir('collectd/rrd/') :
			print domain
			r = RRD('collectd/rrd/%s/load/load.rrd' % domain)
			print r.info()

	chrono = time.time()
	info()
	print (time.time() -chrono) *1000 , 'ms'