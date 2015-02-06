__author__ = 'Jableader'

from django import template
register = template.Library()

from django.utils.html import escape
from django.utils.safestring import mark_safe
from keyword import kwlist

import re
keywords = re.compile('\\b(' + '|'.join(kwlist) + ')\\b')
comments = re.compile('#.*\n')
strings = re.compile('(\'|").*\\1')
digit = re.compile('\d+')
word_regex = re.compile(r"\w+")

def span(klass, contents):
    return '<span class="%s">%s</span>' % (klass, contents)

def index_of(f, collection, i=0):
    while i < len(collection) and not f(collection[i], i):
        i += 1
    return i

def format(s):
    if s == '':
        return ''
    if s[0] in ('\r', '\n'):
        return format(s[1:])
    elif s[0] == '\t':
        return '&nbsp'*4 + format(s[1:])
    elif s[0] == ' ':
        how_many = index_of(lambda char, i: char != ' ', s)
        return '&nbsp'*how_many + format(s[how_many:])
    elif s[0] in ('"', "'"):
        s_end = index_of(lambda char, i: char == s[0] and s[i-1] != '\\', s, 1)
        return span('string', s[:s_end]) + format(s[s_end:])
    elif s[0].isdigit():
        end = index_of(lambda c, i: not c.isdigit(), s)
        return span('digit', s[:end]) + format(s[end:])
    elif s[0] == '#':
        end = 1 + s.index('\n')
        return span('comment', s[:end]) + format(s[end:])
    else:
        match = word_regex.match(s)
        if match:
            if match.group() in kwlist:
                return span("keyword", match.group()) + format(s[match.end():])
            else:
                return match.group() + format(s[match.end():])
        else:
            return s[0] + format(s[1:])

span_base = ''

@register.filter
def as_code(value):
    return mark_safe(format(value))
