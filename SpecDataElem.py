from TableEntry import *
from odict import OrderedDict
import re
import SpecMachine
import SpecProcessor
import SpecDataCores
import SpecL1Cache
import SpecL2Cache
import SpecL3Cache
 
class SpecDataElem(TableEntry):
    "A generic class that holds spec data for a given processor"
    def __init__(self, attrs=None, tests=None):
        if attrs == None:
            attrs = OrderedDict()
            attrs["manufacturer"] = "NA"
            attrs["family"] = "NA"
            attrs["model"] = "NA"
            #attrs["model_default"] = "NA"
            attrs["processor_description"] = "NA"
            attrs["clock"] = "NA"
            attrs["bus"] = "NA"
            attrs["hw_nthreadspercore"] = 0
            attrs["hw_ncoresperchip"] = 0 
            attrs["hw_nchips"] = 0 
            attrs["hw_ncores"] = 0
            attrs["L1I"] = 0
            attrs["L1D"] = 0
            attrs["L1_description"] = "NA"
            attrs["L2"] = 0
            attrs["L2_description"] = "NA"
            attrs["L3"] = 0
            attrs["L3_description"] = "NA"
            attrs["hw_avail"] = 0
            attrs["test_sponsor"] = 0
            attrs["hw_model"] = 0
            attrs["sw_auto_parallel"] = "NA"
            attrs["basemean"] = 0
            attrs["peakmean"] = 0
            if tests != None:
                for test in tests:
                    attrs[test] = 0
            attrs["link"] = "NA"

        TableEntry.__init__(self, attrs)


    def update(self, attr, data, allowDup=False):
        if attr == "hw_model":
            #m = SpecMachine.SpecMachine(data)
            #TableEntry.update(self, "clock", m.clock())
            #TableEntry.update(self, "processor", m.proc())
            #TableEntry.update(self, "hw_model", m.hw())
            TableEntry.update(self, attr, data)
            print data
        elif attr == "CPU Name:" or attr == "CPU:":
            p = SpecProcessor.SpecProcessor(data)
            TableEntry.update(self, "manufacturer", p.make())
            TableEntry.update(self, "family", p.family())
            TableEntry.update(self, "model", p.model())
            #TableEntry.update(self, "model_default", 
            #                  p.family() + ":" + p.clk())
            TableEntry.update(self, "processor_description", p.misc())
            TableEntry.update(self, "bus", p.bus())
            TableEntry.update(self, "clock", p.clk())
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
            TableEntry.update(self, attr, data, allowDup)

