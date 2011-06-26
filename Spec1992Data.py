from SpecDataBase import *
import SpecDataElem
import Table
from odict import OrderedDict
import re
import urllib
import BeautifulSoup
import utils
import pdb

class Spec1992Data(SpecDataBase):
    "A class that parses and holds spec1992 data" 
    def __init__(self, soup, elem=SpecDataElem):
        self.__hdrMap = {'By:' : 'test_sponsor',
                         'Model Number'  : 'hw_model',
                         'Number of CPUs': 'hw_nchips'
                         }
        SpecDataBase.__init__(self, soup, elem=elem)

    def htmlTables(self, soup):
        tabs = [soup.h2]
        return tabs


    def parseTable(self, tab):
        table = Table.Table(str(tab.text), self.getElem()().attrs())

        line = tab.findNext("pre").findNext("a")

        linecnt = 0

        while line:
            saveData = self.getElem()()
            error = False

            link = str(line['href'])
            print "found link=" + link

            html = urllib.urlopen(link).read()
            soup = BeautifulSoup.BeautifulSoup(html)
            saveData.update("link", link)
            error = self.__parseDetails__(saveData, soup)
            linecnt += 1
            if error:
                print "Warning: skipping line due to error"
            else:
                table.addEntry(saveData)

            line = line.findNext("a")

            #if linecnt >= 5:
            #    break

        return table



    def __parseDetails__(self, saveData, soup):

        error = False

        perf = soup.pre.findNext("pre")
        tab = re.split("\n", str(perf.text))

        # remove the first 4 lines (header garbage)
        tab.pop(0)
        tab.pop(0)
        tab.pop(0)
        tab.pop(0)

        # write test results
        for test in tab:
            results = test.split()
            saveData.update(results[0], results[4])

        # save summary results
        summary = re.split(":", str(perf.findNext("dd").text))
        if len(summary) > 1:
            saveData.update(summary[0].strip(), summary[1].strip())

        summary = re.split(":", str(perf.findNext("dd").findNext("dd").text))
        if len(summary) > 1:
            saveData.update(summary[0].strip(), summary[1].strip())
        

        info = perf.findNext("pre").findNext("pre").dd

        #pdb.set_trace()

        #write dd attributes
        while info:
            attrs = re.split(":", str(info.text))
            if len(attrs) > 1:
                attr = attrs[0].strip()
                val  = attrs[1].strip()
                if info.dd:
                    attrNext = re.split(":", str(info.dd.text))[0]
                    try:
                        val = re.sub(attrNext, "", val)
                    except:
                        print "skipping ", attrNext

                if not attr in saveData.tests():
                    #print "saving ", attr
                    saveData.update(attr, val)
            info = info.dd

        
        # write dt attributes
        info = perf.findNext("pre").findNext("pre").dt
        while info:
            attrs = re.split(":", str(info.text))
            if len(attrs) > 1:
                attr = attrs[0].strip()
                val  = attrs[1].strip()
                if info.dt:
                    attrNext = re.split(":", str(info.dt.text))[0]
                    val = re.sub(attrNext, "", val)

                if not attr in saveData.tests():
                    #print "saving ", attr
                    saveData.update(attr, val)
            info = info.dt

        return error

