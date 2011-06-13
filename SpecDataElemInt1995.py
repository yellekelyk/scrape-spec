from SpecDataElem1995 import *

class SpecDataElemInt1995(SpecDataElem1995):
    "A class that holds spec int data for a given processor"

    def __init__(self):
        tests = ["099_go",
                 "124_m88ksim",
                 "126_gcc",
                 "129_compress",
                 "130_li",
                 "132_ijpeg",
                 "134_perl", 
                 "147_vortex"] 

        attrMap = {"099 Base": "099_go",
                   "124 Base": "124_m88ksim",
                   "126 Base": "126_gcc",
                   "129 Base": "129_compress",
                   "130 Base": "130_li",
                   "132 Base": "132_ijpeg",
                   "134 Base": "134_perl",
                   "147 Base": "147_vortex"}

        SpecDataElem1995.__init__(self, tests=tests, attrMap=attrMap)




    
