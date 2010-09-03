__author__ = "mathieu@garambrogne.net"
__version__ = "0.1"

from datetime import datetime

def none_filter(stuff):
	"A dummy filter wich does nothing"
	return stuff

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
