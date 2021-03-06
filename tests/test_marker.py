__author__ = 'Jableader'

from django.test import SimpleTestCase
from golfsite.models import Submission
from golfsite.markers import LineCounter
from test_suite import asset
from django.core.files import File as DjangoFile
from django.core.files.base import File as ContentFile

class TestLineCounter(SimpleTestCase):

    def test_markSizeFromFile(self):
        with open(asset('hello_world.py'), 'r') as fp:
            self.assertEqual(1, LineCounter().mark_size(Submission(file=DjangoFile(fp))))