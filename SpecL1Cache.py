import pdb
import re
from SpecCache import *

class SpecL1Cache(SpecCache):
    "A class to aid in parsing spec caches, which can be in a number of forms"
    def __init__(self, string):
        self.__sizeI  = "NA"
        self.__sizeD  = "NA"
        
        # remove all parentheses before parsing
        string = string.replace('(','')
        string = string.replace(')','')

        SpecCache.__init__(self, string)

        for match in self.matches():
            size = int(match[0]) * self.toKB(match[1])
            if match[2] == "i":
                self.__sizeI = size
            elif match[2] == "d":
                self.__sizeD = size
            else:
                # we assume it's i+d
                raise Exception("Unexpected L1Cache string: " + string)

    def L1I(self):
        return self.__sizeI

    def L1D(self):
        return self.__sizeD
