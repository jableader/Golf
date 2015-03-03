__author__ = 'Jableader'

import logging
logger = logging.getLogger()

#Markers for submissions
import re
_whitespace_regex = re.compile('^\\s*$')


class LineCounter:
    def mark_size(self, submission):
        submission.file.open('r')
        try:
            return self.mark_size_core(submission.file)

        except IOError:
            logging.log(msg='Could not mark %d' % submission.pk)
            return None
        finally:
            submission.file.close()

    def mark_size_core(self, filePointer):
        return len([l for l in filePointer.readlines() if _whitespace_regex.match(l) is None])