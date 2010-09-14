#!/usr/bin/env python
import sys
sys.path.append('../src')

import unittest
import os
import os.path
from datetime import datetime

from roundrobin.rrd import create, COUNTER, AVERAGE
from roundrobin import query

class BasicTest(unittest.TestCase):
	"""
	http://oss.oetiker.ch/rrdtool/tut/rrdtutorial.en.html
	"""
	def setUp(self):
		FILE = 'test.rrd'
		if os.path.exists(FILE):
			os.remove(FILE)
		self.rrd = create(FILE, [COUNTER('speed', 600, 'U','U'), AVERAGE(0.5,1,24), AVERAGE(0.5, 6, 10)], start=920804400)
		self.assertTrue(os.path.exists(FILE))
		self.rrd.update([
		(920804700, 12345),
		(920805000, 12357),
		(920805300, 12363),
		(920805600, 12363),
		(920805900, 12363),
		(920806200, 12373),
		(920806500, 12383),
		(920806800, 12393),
		(920807100, 12399),
		(920807400, 12405),
		(920807700, 12411),
		(920808000, 12415),
		(920808300, 12420),
		(920808600, 12422),
		(920808900, 12423)])
	def _test_info(self):
		print self.rrd.info()
	def test_query(self):
		q = query.AVERAGE(start=920804400, end=920809200, column=0, filter = lambda data: (1 - data))
		data = [(ts, value) for ts, value in q(self.rrd)]
		#print data, len(data)
		self.assertEqual(None, data[0][1])
		self.assertEqual(None, data[-1][1])
		self.assertEqual(None, data[-2][1])
		self.assertEqual(17, len(data))
		#self.assertEqual(None, data[-1][1])
	def test_update(self):
		self.rrd.updateOnce(920809200, 12415)
		self.rrd.updateOnce(datetime.fromtimestamp(920809500), 12430)
if __name__ == '__main__':
    unittest.main()