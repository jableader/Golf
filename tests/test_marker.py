from unittest import TestCase
import random
from GolfServer.markers import *
__author__ = 'Jableader'

class TestLineCounter(TestCase):
    def test_markSize(self):
        marker = LineCounter()
        random.seed(1234)
        lines = [[' ', '\t']*random.randint(0, 10) for j in xrange(10)]
        lines = map(lambda l: ''.join(l), lines)
        lines[4] = 'print("Hello World")'

        self.assertEqual(1, marker.marksize('\r\n'.join(lines)))