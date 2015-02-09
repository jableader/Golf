__author__ = 'Jableader'
from django.test import SimpleTestCase
from GolfServer.templatetags.codify import as_code, format
from keyword import kwlist
import re

class CodifyTests(SimpleTestCase):
    def assertSpanClass(self, klass, code):
        self.assertEqual(klass, re.match(r'^<span class="(\w+)"', format(code)).group(1))

    def test_colors(self):
        base = '<span class="keyword">%s</span>'
        for keyword in kwlist:
            self.assertEqual(base % keyword, format(keyword))

    def test_injection(self):
        s = 's = "<a href="naughty_site.com">Click Me!</a>'

        try:
            format(s).index('<a ')
            self.fail("Should not contain the substring")
        except ValueError:
            #index error means it got escaped
            pass

    def test_overlap(self):
        self.assertEqual(format('"32"'), '<span class="string">&quot;32&quot;</span>')
        self.assertEqual(format('#"32"'), '<span class="comment">#&quot;32&quot;</span>')

    def test_no_end_quote(self):
        #Since the uploaded code is broken, idc how it gets rendered
        #However it should not break the application

        format('')

    def test_doesnt_throw_exception_on_all_kinds_of_endings(self):
        format('word')
        format('10')
        format('"string"')
        format('"candleja') #open string
        format('"""BigString"""')
        format('#Comment')
        format(' ')
        format('\t')
        format('\n')
        format('=')

