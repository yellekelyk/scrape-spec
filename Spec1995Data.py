from SpecDataBase import *
import SpecDataElem
import Table
from odict import OrderedDict
import re

class Spec1995Data(SpecDataBase):
    "A class that parses and holds spec1995 data" 
    def __init__(self, soup):
        self.__hdrMap = {'Company' : 'test_sponsor',
                         'System'  : 'hw_model',
                         '# CPU'   : 'hw_nthreadspercore',
                         'Baseline': 'basemean',
                         'Result'  : 'peakmean'}
        SpecDataBase.__init__(self, soup)

    def htmlTables(self, soup):
        tabs = soup.findAll("h3")
        return tabs


    def parseTable(self, tab):
        name = str(tab.text)
        table = Table.Table(name, SpecDataElem.SpecDataElem().attrs())

        pre = tab.findNext("pre")
        lines = str.split(str(''.join(pre.findAll(text=True))),"\n")
        lines.remove(lines[0])
        
        reSplit = re.compile("\s\s+")

        #determine hdr order
        hdr = list()
        for txt in reSplit.split(lines[1]):
            hdr.append(txt.strip())

        lines.remove(lines[1])
        #loop through all lines in table 
        for line in lines:
            saveData = SpecDataElem.SpecDataElem()
            fields = reSplit.split(line)
            saveData.update("hw_ncoresperchip", 1)

            if len(fields) == 6:
                saveData.update("test_sponsor",       fields[0])
                saveData.update("hw_model",           fields[1])
                saveData.update("peakmean",           fields[2])
                saveData.update("basemean",           fields[3])
                saveData.update("hw_nchips",          fields[4])
            elif len(fields) > 6:
                fields.pop(len(fields)-1)
                saveData.update("test_sponsor", fields.pop(0))
                # now proceed from the end
                saveData.update("hw_nchips", fields.pop(len(fields)-1))
                saveData.update("basemean", fields.pop(len(fields)-1))
                saveData.update("peakmean", fields.pop(len(fields)-1))
                saveData.update("hw_model", ' '.join(fields))
            else:
                print( "Bad row: " + line)
            table.addEntry(saveData)

        return table
