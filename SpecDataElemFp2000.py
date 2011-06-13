from SpecDataElem import *

class SpecDataElemFp2000(SpecDataElem):
    "A class that holds spec fp data for a given processor"

    def __init__(self):

        tests = ["168.wupwise",
                 "171.swim",
                 "172.mgrid",
                 "173.applu",
                 "177.mesa",
                 "178.galgel",
                 "179.art",
                 "183.equake",
                 "187.facerec",
                 "188.ammp",
                 "189.lucas",
                 "191.fma3d",
                 "200.sixtrack",
                 "301.apsi"]

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
