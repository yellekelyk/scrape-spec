from SpecDataBase import *
import SpecDataElem
import Table
from odict import OrderedDict

class Spec2006Data(SpecDataBase):
    "A class that parses and holds spec2006 data" 

    def __init__(self, soup):
        SpecDataBase.__init__(soup)

    def htmlTables(self, soup):
        return soup.findAll(attrs={"class":"idx_table"})


    def parseTable(self, tab):
        table = Table.Table(str(tab.a.text), 
                            SpecDataElem.SpecDataElem().attrs())
        headers = OrderedDict()
        hdrs = tab.findAll(attrs={"class":"header"})
        for hdr in hdrs:
            next = hdr.th
            while next:
                try:
                    headers[str(next.get("class"))] = 0
                except AttributeError:
                    pass
                next = next.nextSibling


        line = tab.tbody.tr
        #loop through all lines in table 
        while line:
            # ignore intertable headers
            if line.get("class") != "intertable odd header":
                saveData = SpecDataElem.SpecDataElem()
                entry = line.td
                while entry:
                    if entry != '\n': 
                        attr = entry.get("class")
                        data = str(entry.text)
                        if entry.firstText() != None:
                            tmp = entry.firstText()
                            data = str(tmp.previousSibling)

                        data = data.replace('&nbsp;', '')
                        saveData.update(attr,data) 
                    entry = entry.nextSibling
                table.addEntry(saveData)

            # go to next line
            line = line.findNextSibling("tr")
        
        return table
