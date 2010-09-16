from TableEntry import *
from odict import OrderedDict
import re
import SpecMachine
import SpecDataCores
 
class SpecDataElem(TableEntry):
    "A generic class that holds spec data for a given processor"
    def __init__(self, attrs=None):
        if attrs == None:
            attrs = OrderedDict()
            attrs["test_sponsor"] = 0
            attrs["hw_model"] = 0
            attrs["processor"] = 0
            attrs["clock"] = "NA"
            attrs["hw_nthreadspercore"] = 0
            attrs["hw_ncoresperchip"] = 0 
            attrs["hw_nchips"] = 0 
            attrs["hw_ncores"] = 0
            attrs["basemean"] = 0
            attrs["peakmean"] = 0

        TableEntry.__init__(self, attrs)


    def update(self, attr, data):
        if attr == "hw_model":
            m = SpecMachine.SpecMachine(data)
            TableEntry.update(self, "clock", m.clock())
            TableEntry.update(self, "processor", m.proc())
            TableEntry.update(self, "hw_model", m.hw())

        elif attr == "hw_nthreadspercore":
            c = SpecDataCores.SpecDataCores(data)
            TableEntry.update(self, "hw_nthreadspercore", c.thrdsPerCore())
            TableEntry.update(self, "hw_ncoresperchip",   c.coresPerChip())
            TableEntry.update(self, "hw_nchips",    c.chipsTotal())
            TableEntry.update(self, "hw_ncores", c.coresTotal())

        else:
            TableEntry.update(self, attr, data)

