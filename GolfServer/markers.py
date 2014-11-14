__author__ = 'Jableader'

#Markers for submissions

class LineCounter:
    def marksize(self, filePointer):
        return reduce(lambda sum, line:  sum+1, filePointer, 0)