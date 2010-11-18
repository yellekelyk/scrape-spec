import re
from SpecCache import *

class SpecL3Cache(SpecCache):
    "A class to aid in parsing spec L3 caches, which can be in a number of forms"
    def __init__(self, string):
        self.__size  = "NA"
        
        SpecCache.__init__(self, string)

        for match in self.matches("(\d+)\s*([kmg]b)\s*(i\s*\+\s*d)"):
            size = int(match[0]) * self.toKB(match[1])
            self.__size = size

    def L3(self):
        return self.__size

