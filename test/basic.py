#!/usr/bin/env python
import sys
sys.path.append('../src')

from roundrobin.rrd import RRD
import unittest
import os
import os.path

class BasicTest(unittest.TestCase):
	def setUp(self):
		if os.path.exists('test.rrd'):
			os.remove('test.rrd')
		self.rrd = RRD('test.rrd')
		self.rrd._create('--start 920804400 DS:speed:COUNTER:600:U:U RRA:AVERAGE:0.5:1:24 RRA:AVERAGE:0.5:6:10')
		self.rrd._update('920804700:12345 920805000:12357 920805300:12363')
		self.rrd._update('920805600:12363 920805900:12363 920806200:12373')
		self.rrd._update('920806500:12383 920806800:12393 920807100:12399')
		self.rrd._update('920807400:12405 920807700:12411 920808000:12415')
		self.rrd._update('920808300:12420 920808600:12422 920808900:12423')
	def test_info(self):
		print self.rrd.info()

if __name__ == '__main__':
    unittest.main()