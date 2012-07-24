from SpecDataElem1995 import *

class SpecDataElemInt1995(SpecDataElem1995):
    "A class that holds spec int data for a given processor"

    def __init__(self):
        tests = ["099.go",
                 "124.m88ksim",
                 "126.gcc",
                 "129.compress",
                 "130.li",
                 "132.ijpeg",
                 "134.perl", 
                 "147.vortex"] 

        attrMap = {"099 Base": "099.go",
                   "124 Base": "124.m88ksim",
                   "126 Base": "126.gcc",
                   "129 Base": "129.compress",
                   "130 Base": "130.li",
                   "132 Base": "132.ijpeg",
                   "134 Base": "134.perl",
                   "147 Base": "147.vortex"}

        SpecDataElem1995.__init__(self, tests=tests, attrMap=attrMap)




    
