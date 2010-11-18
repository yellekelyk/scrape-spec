from SpecDataElem import *

class SpecDataElemFp(SpecDataElem):
    "A class that holds spec fp data for a given processor"

    def __init__(self):
        tests = ["410.bwaves",
                 "416.gamess",
                 "433.milc",  
                 "434.zeusmp",   
                 "435.gromacs",  
                 "436.cactusADM", 
                 "437.leslie3d",
                 "444.namd",
                 "447.dealII",
                 "450.soplex",  
                 "453.povray",  
                 "454.calculix",
                 "459.GemsFDTD",
                 "465.tonto",
                 "470.lbm",   
                 "481.wrf",     
                 "482.sphinx3"]

        SpecDataElem.__init__(self, tests=tests)


