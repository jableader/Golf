__author__ = 'Jableader'

from django import template
register = template.Library()

from django.utils.html import escape
from django.utils.safestring import mark_safe
from keyword import kwlist

import re
word_regex = re.compile(r"\w+")

def span(klass, contents):
    return '<span class="%s">%s</span>' % (klass, escape(contents))

def index_of(f, collection, i=0):
    while i < len(collection) and not f(collection[i], i):
        i += 1
    return i

def format(s):
    index = lambda f, i=0: index_of(f, s, i)
    count = lambda desired, i=0: index_of(lambda actual, i: actual != desired, s)

    if s == '':
        return ''
    if s[0] in ('\r', '\n'):
        return format(s[1:])
    elif s[0] == '\t':
        cnt = count('\t')
        return '&nbsp'*4 * cnt + format(s[cnt:])
    elif s[0] == ' ':
        cnt = count(' ')
        return '&nbsp'*cnt+ format(s[cnt:])
    elif s[0] in ('"', "'"):
        s_end = index(lambda c, i: c == s[0] and s[i-1] != '\\', 1) + 1
        return span('string', s[:s_end]) + format(s[s_end:])
    elif s[0].isdigit():
        end = index(lambda c, i: not c.isdigit())
        return span('digit', s[:end]) + format(s[end:])
    elif s[0] == '#':
        end = index(lambda c, i: c == '\n')
        return span('comment', s[:end]) + format(s[end:])
    else:
        match = word_regex.match(s)
        if match:
            if match.group() in kwlist:
                return span("keyword", match.group()) + format(s[match.end():])
            else:
                return match.group() + format(s[match.end():])
        else:
            return escape(s[0]) + format(s[1:])

@register.filter
def as_code(value):
    return mark_safe(format(value))
