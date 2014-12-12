__author__ = 'Jableader'

#Markers for submissions
import re
_whitespace_regex = re.compile('\n\\s*\n')

def _remove_blank_lines(string):
    return _whitespace_regex.sub('\n', string).strip()

class LineCounter:

    def marksize(self, contents):
        contents = _remove_blank_lines(contents)

        return reduce(lambda sum, line:  sum+1, _remove_blank_lines(contents).splitlines(), 0)