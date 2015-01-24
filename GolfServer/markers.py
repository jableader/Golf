__author__ = 'Jableader'

import logging
logger = logging.getLogger()

#Markers for submissions
import re
_whitespace_regex = re.compile('^\\s*$')

def mark_size(submission):
    submission.file.open('r')
    try:
        return __count_non_whitespace_lines(submission.file)

    except IOError:
        logging.log(msg='Could not mark %d' % submission.pk)
        return 0
    finally:
        submission.file.close()


def __count_non_whitespace_lines(filePointer):
    return len([l for l in filePointer.readlines() if _whitespace_regex.match(l) is None])