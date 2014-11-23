from unittest import TestCase
from GolfServer.markers import *
__author__ = 'Jableader'

class TestLineCounter(TestCase):
    def test_markSize(self):
        marker = LineCounter()
        self.assertEqual(5, marker.marksize(['']*5))