from SpecDataElem import *

class SpecDataElemInt2000(SpecDataElem):
    "A class that holds spec int data for a given processor"

    def __init__(self):
        tests = ["164.gzip",
                 "175.vpr",
                 "176.gcc",
                 "181.mcf",
                 "186.crafty",
                 "197.parser",
                 "252.eon",
                 "253.perlbmk",
                 "254.gap",
                 "255.vortex",
                 "256.bzip2",
                 "300.twolf"]
    
        SpecDataElem.__init__(self, tests=tests)


    def update(self, attr, data):
        if attr == "hw_nthreadspercore":
            c = SpecDataCores.SpecDataCores(data)
            TableEntry.update(self, "hw_nthreadspercore", c.thrdsPerCore())
            TableEntry.update(self, "hw_ncoresperchip",   c.coresPerChip())
            TableEntry.update(self, "hw_nchips",    c.chipsTotal())
            TableEntry.update(self, "hw_ncores", c.coresTotal())
        else:
            SpecDataElem.update(self, attr, data)
