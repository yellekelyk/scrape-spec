from SpecDataBase import *
import SpecDataElem
import Table
from odict import OrderedDict

class Spec2000Data(SpecDataBase):
    "A class that parses and holds spec2000 data" 
    def __init__(self, soup):
        self.__hdrMap = {'Company Name': 'test_sponsor',
                         'System Name' : 'hw_model',
                         '#CPU'        : 'hw_nthreadspercore',
                         'Base'        : 'basemean',
                         'Peak'        : 'peakmean'}
        SpecDataBase.__init__(self, soup)

    def htmlTables(self, soup):
        tabs = soup.findAll("h3")
        return tabs


    def parseTable(self, tab):
        name = str(tab.text)
        table = Table.Table(name, SpecDataElem.SpecDataElem().attrs())

        #determine hdr order
        hdrInfo  = tab.findNext("tr").th
        hdr = list()
        while hdrInfo:
            hdr.append(str(hdrInfo.text))
            hdrInfo = hdrInfo.findNextSibling("th")

        #loop through all lines in table 
        line = tab.findNext("tr").findNext("tr")
        while line:
            saveData = SpecDataElem.SpecDataElem()

            info = line.td
            cnt  = 0
            while info:
                #print(info)
                if hdr[cnt] in self.__hdrMap:
                    attr = self.__hdrMap[hdr[cnt]]
                    data = str(info.text)
                    saveData.update(attr, data)
                    cnt = cnt + 1
                info = info.findNextSibling("td")
            table.addEntry(saveData)

            # go to next line
            line = line.findNext("tr")
        
        return table
