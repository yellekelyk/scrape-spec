from SpecDataElem import *

class SpecDataElemInt2006(SpecDataElem):
    "A class that holds spec int data for a given processor"

    def __init__(self):
        tests = ["400.perlbench", 
                 "401.bzip2", 
                 "403.gcc", 
                 "429.mcf", 
                 "445.gobmk", 
                 "456.hmmer", 
                 "458.sjeng", 
                 "462.libquantum", 
                 "464.h264ref", 
                 "471.omnetpp", 
                 "473.astar", 
                 "483.xalancbmk"]
    
        SpecDataElem.__init__(self, tests=tests)


