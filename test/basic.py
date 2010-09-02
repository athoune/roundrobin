import sys
sys.path.append('../src')

from roundrobin.rrd import RRD, rrd_wrapper
import unittest
from subprocess import Popen
import os

class BasicTest(unittest.TestCase):
	def setUp(self):
		rrd_wrapper('create test.rrd --start 920804400 DS:speed:COUNTER:600:U:U RRA:AVERAGE:0.5:1:24 RRA:AVERAGE:0.5:6:10')
		rrd_wrapper('update test.rrd 920804700:12345 920805000:12357 920805300:12363')
		rrd_wrapper('update test.rrd 920805600:12363 920805900:12363 920806200:12373')
		rrd_wrapper('update test.rrd 920806500:12383 920806800:12393 920807100:12399')
		rrd_wrapper('update test.rrd 920807400:12405 920807700:12411 920808000:12415')
		rrd_wrapper('update test.rrd 920808300:12420 920808600:12422 920808900:12423')
	def test_info(self):
		r = RRD('test.rrd')
		print r.info()

if __name__ == '__main__':
    unittest.main()