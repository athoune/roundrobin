import sys
sys.path.append('../src')

from roundrobin.rrd import RRD
import unittest
from subprocess import Popen
import os

class BasicTest(unittest.TestCase):
	def setUp(self):
		env = os.environ
		env['LC_NUMERIC'] = 'en_US'
		Popen('rrdtool  create test.rrd --start 920804400 DS:speed:COUNTER:600:U:U RRA:AVERAGE:0.5:1:24 RRA:AVERAGE:0.5:6:10', env= env, shell=True)
	def test_info(self):
		pass

if __name__ == '__main__':
    unittest.main()