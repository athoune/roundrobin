__author__ = "mathieu@garambrogne.net"
__version__ = "0.1"

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

class Result(object):
	"Querying a round robin database return a Result"
	def __init__(self, raw, column = 0, filter = none_filter):
		self.raw = raw
		self.column = column
		self.filtr = filter
	def __iter__(self):
		cpt = 0
		for line in self.raw:
			cpt += 1
			if cpt > 2:
				ts, values = line.split(': ',1)
				dt = datetime.fromtimestamp(int(ts))
				value = values.split(' ')
				if value == 'nan':
					yield dt,  None
				if self.column != None:
					yield dt, self.filtr(float(value[self.column]))
				else:
					yield dt, self.filtr(map(float_or_none, value))
