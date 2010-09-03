__author__ = "mathieu@garambrogne.net"
__version__ = "0.1"

from result import none_filter

class Query(object):
	"Querying round robin database"
	def __init__(self, consolidation='AVERAGE', resolution=None, start=None,
			end=None, filter=none_filter, column=None):
		self.consolidation = consolidation
		self.resolution = resolution
		self.start = start
		self.end = end
		self.filter = filter
		self.column = column
	def command(self):
		"command line option for 'rrd fetch'"
		buff = self.consolidation
		if self.resolution != None:
			buff += ' -r %i' % self.resolution
		if self.start != None:
			buff += ' -s %s' % self.start
		if self.end != None:
			buff += ' -e %s' % self.end
		return buff
	def __call__(self, rrd):
		return rrd._query(self.command(), self.column, self.filter)

def AVERAGE(**args):
	"Average query"
	return Query('AVERAGE', **args)
def MIN(**args):
	"Min query"
	return Query('MIN', **args)
def MAX(**args):
	"Max query"
	return Query('MAX', **args)
def LAST(**args):
	"Last query"
	return Query('LAST', **args)

