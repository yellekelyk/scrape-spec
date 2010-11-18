from TableEntry import *
from odict import OrderedDict
import re
import SpecMachine
import SpecDataCores
import SpecL1Cache
import SpecL2Cache
import SpecL3Cache
 
class SpecDataElem(TableEntry):
    "A generic class that holds spec data for a given processor"
    def __init__(self, attrs=None, tests=None):
        if attrs == None:
            attrs = OrderedDict()
            attrs["hw_avail"] = 0
            attrs["test_sponsor"] = 0
            attrs["hw_model"] = 0
            attrs["processor"] = 0
            attrs["processor_description"] = "NA"
            attrs["clock"] = "NA"
            attrs["hw_nthreadspercore"] = 0
            attrs["hw_ncoresperchip"] = 0 
            attrs["hw_nchips"] = 0 
            attrs["hw_ncores"] = 0
            attrs["sw_auto_parallel"] = "NA"
            attrs["basemean"] = 0
            attrs["peakmean"] = 0
            attrs["L1I"] = 0
            attrs["L1D"] = 0
            attrs["L1_description"] = "NA"
            attrs["L2"] = 0
            attrs["L2_description"] = "NA"
            attrs["L3"] = 0
            attrs["L3_description"] = "NA"
            attrs["link"] = "NA"
            #attrs["results"] = Table.Table()
            if tests != None:
                for test in tests:
                    attrs[test] = 0
                    #for bp in ["base", "peak"]:
                    #attrs[str(test + "." + bp)] = 0

        TableEntry.__init__(self, attrs)


    def update(self, attr, data):
        if attr == "hw_model":
            m = SpecMachine.SpecMachine(data)
            TableEntry.update(self, "clock", m.clock())
            TableEntry.update(self, "processor", m.proc())
            TableEntry.update(self, "hw_model", m.hw())
            print data

        #elif attr == "hw_nthreadspercore":
        #    c = SpecDataCores.SpecDataCores(data)
        #    TableEntry.update(self, "hw_nthreadspercore", c.thrdsPerCore())
        #    TableEntry.update(self, "hw_ncoresperchip",   c.coresPerChip())
        #    TableEntry.update(self, "hw_nchips",    c.chipsTotal())
        #    TableEntry.update(self, "hw_ncores", c.coresTotal())

        elif attr == "CPU Name:" or attr == "CPU:":
            TableEntry.update(self, "processor", data, allowDup=True)
        elif attr == "CPU Characteristics:":
            TableEntry.update(self, "processor_description", data)
        elif attr == "CPU MHz:":
            TableEntry.update(self, "clock", data, allowDup=True)
        elif attr == "Parallel:":
            TableEntry.update(self, "sw_auto_parallel", data, allowDup=True)
        elif attr == "Primary Cache:":
            c = SpecL1Cache.SpecL1Cache(data)
            TableEntry.update(self, "L1D", c.L1D())
            TableEntry.update(self, "L1I", c.L1I())
            TableEntry.update(self, "L1_description", c.description())
        elif attr == "Secondary Cache:":
            c = SpecL2Cache.SpecL2Cache(data)
            TableEntry.update(self, "L2", c.L2())
            TableEntry.update(self, "L2_description", c.description())
        elif attr == "L3 Cache:":
            c = SpecL3Cache.SpecL3Cache(data)
            TableEntry.update(self, "L3", c.L3())
            TableEntry.update(self, "L3_description", c.description())

        #else:
        #    print str("DEBUG-unknown attr " + attr)

        else:
            TableEntry.update(self, attr, data)

