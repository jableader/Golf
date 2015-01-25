__author__ = 'Jableader'

from django import template
register = template.Library()

from django.utils.html import escape
from django.utils.safestring import mark_safe

import re
space_regex = re.compile(' {4}|\t')

@register.filter
def as_code(value):
    return mark_safe(space_regex.sub('&nbsp;'*4, escape(value)))