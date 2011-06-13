from SpecDataElem1995 import *

class SpecDataElemFp1995(SpecDataElem1995):
    "A class that holds spec int data for a given processor"

    def __init__(self):
        tests = ["101_tomcatv",
                 "102_swim",
                 "103_su2cor",
                 "104_hydro2d",
                 "107_mgrid",
                 "110_applu",
                 "125_turb3d",
                 "141_apsi",
                 "145_fpppp",
                 "146_wave5"]   

        attrMap = {"101 Base": "101_tomcatv",
                   "102 Base": "102_swim",
                   "103 Base": "103_su2cor",
                   "104 Base": "104_hydro2d",
                   "107 Base": "107_mgrid",
                   "110 Base": "110_applu",
                   "125 Base": "125_turb3d",
                   "141 Base": "141_apsi",
                   "145 Base": "145_fpppp",
                   "146 Base": "146_wave5"}

        SpecDataElem1995.__init__(self, tests=tests, attrMap=attrMap)




    
