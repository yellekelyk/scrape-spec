from SpecDataElem1992 import *

class SpecDataElemFp1992(SpecDataElem1992):
    "A class that holds spec int data for a given processor"

    def __init__(self):
        tests = ["013.spice2g6",
                 "015.doduc",   
                 "034.mdljdp2", 
                 "039.wave5",   
                 "047.tomcatv", 
                 "048.ora",
                 "052.alvinn",  
                 "056.ear",
                 "077.mdljsp2",
                 "078.swm256",
                 "089.su2cor",
                 "090.hydro2d",
                 "093.nasa7",
                 "094.fpppp"]

        self.__tests = tests

        attrMap = {"SPECfp92" : "peakmean",
                   "SPECbase_fp92" : "basemean"}
        #attrMap = {"101 Base": "101_tomcatv",
        #           "102 Base": "102_swim",
        #           "103 Base": "103_su2cor",
        #           "104 Base": "104_hydro2d",
        #           "107 Base": "107_mgrid",
        #           "110 Base": "110_applu",
        #           "125 Base": "125_turb3d",
        #           "141 Base": "141_apsi",
        #           "145 Base": "145_fpppp",
        #           "146 Base": "146_wave5"}

        SpecDataElem1992.__init__(self, tests=tests, attrMap=attrMap)


    def tests(self):
        return self.__tests

    
