__author__ = 'Jableader'
from django.test import SimpleTestCase
from GolfServer.templatetags.codify import color_code
from keyword import kwlist

class CodeifyTests(SimpleTestCase):

    def test_colors(self):
        base = '<span class="keyword">%s</span>'
        for keyword in kwlist:
            self.assertEqual(base % keyword, color_code(keyword))

