#!/usr/bin/env python
import sys
sys.path.append('../src')

from roundrobin.rrd import RRD
from roundrobin.query import AVERAGE
import unittest
import os
import os.path

class BasicTest(unittest.TestCase):
	def setUp(self):
		FILE = 'test.rrd'
		if os.path.exists(FILE):
			os.remove(FILE)
		self.rrd = RRD(FILE)
		self.rrd._create('--start 920804400 DS:speed:COUNTER:600:U:U RRA:AVERAGE:0.5:1:24 RRA:AVERAGE:0.5:6:10')
		self.assertTrue(os.path.exists(FILE))
		self.rrd._update('920804700:12345 920805000:12357 920805300:12363')
		self.rrd._update('920805600:12363 920805900:12363 920806200:12373')
		self.rrd._update('920806500:12383 920806800:12393 920807100:12399')
		self.rrd._update('920807400:12405 920807700:12411 920808000:12415')
		self.rrd._update('920808300:12420 920808600:12422 920808900:12423')
	def test_info(self):
		print self.rrd.info()
	def test_query(self):
		query = AVERAGE(resolution=10, start='-10m', column=0, filter = lambda data: (1 - data))
		for ts, value in query(self.rrd):
			print ts, value

if __name__ == '__main__':
    unittest.main()