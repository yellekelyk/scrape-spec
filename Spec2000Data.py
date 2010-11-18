from SpecDataBase import *
import SpecDataElem
import Table
from odict import OrderedDict
import re
import pdb
import urllib
import BeautifulSoup

class Spec2000Data(SpecDataBase):
    "A class that parses and holds spec2000 data" 
    def __init__(self, soup, elem=SpecDataElem):
        self.__hdrMap = {'Company Name': 'test_sponsor',
                         'System Name' : 'hw_model',
                         '#CPU'        : 'hw_nthreadspercore',
                         'Base'        : 'basemean',
                         'Peak'        : 'peakmean',
                         'Full Disclosures' : 'link'}
        SpecDataBase.__init__(self, soup, elem=elem)

    def htmlTables(self, soup):
        tabs = soup.findAll("h3")
        return tabs


    def parseTable(self, tab):
        name = str(tab.text)
        table = Table.Table(str(tab.text), self.getElem()().attrs())

        #determine hdr order
        hdrInfo  = tab.findNext("tr").th
        hdr = list()
        while hdrInfo:
            hdr.append(str(hdrInfo.text))
            hdrInfo = hdrInfo.findNextSibling("th")

        #loop through all lines in table 
        line = tab.findNext("tr").findNext("tr")

        #pdb.set_trace()
        while line:
            saveData = self.getElem()()

            entry = line.td
            cnt  = 0
            error = False
            while entry:
                #print(entry)
                if hdr[cnt] in self.__hdrMap:
                    attr = self.__hdrMap[hdr[cnt]]
                    data = str(entry.text)

                    if attr == "link":
                        #pdb.set_trace()
                        link = str("http://www.spec.org/cpu2000/results/" + 
                                   str(entry.findNext("a").findNextSibling("a")['href']))
                        data = link
                        html = urllib.urlopen(link).read()
                        soup = BeautifulSoup.BeautifulSoup(html)
                        error = error or self.__parseDetails__(saveData, soup)

                    saveData.update(attr, data)
                    cnt = cnt + 1
                    
                entry = entry.findNextSibling("td")
            if error:
                print "Warning: skipping line due to error"
            else:
                table.addEntry(saveData)

            # go to next line
            line = line.findNext("tr")
        
        return table



    def __parseDetails__(self, saveData, soup):

        error = False

        tab = soup.body.table.findNextSibling("table").findNextSibling("table")
        line = tab.tr.td
        while line:
            check = re.search("Hardware Avail:\s*(\w+-\d+)", str(line.text))
            if check:
                saveData.update("hw_avail", check.group(1))
            line = line.findNextSibling("td")

        tab = tab.findNextSibling("table")
        #determine hdr order of results
        #pdb.set_trace()
        hdrInfo  = tab.findNext("tr").th
        hdr = list()
        while hdrInfo:
            hdr.append(str(hdrInfo.text))
            hdrInfo = hdrInfo.findNextSibling("th")

        # store results
        #pdb.set_trace()
        line = tab.findNext("tr").findNextSibling("tr")
        while line:
            cnt  = 0
            entry = line.td
            #if entry.get("class") != "bm":
            #    raise Exception("Expected class 'bm', got " + 
            #                    entry.get("class"))
            #testName  = str(entry.text).replace('&nbsp;', '')
            #testScore = None

            #we only proceed if there is clearly enough data present
            # (otherwise we might misplace something due to the cnt scheme)
            if len(line.findAll("td")) >= len(hdr):
                testName = None
                testScore = None
                while entry:
                    text = str(entry.text).replace('&nbsp;', '')
                    if cnt < len(hdr):
                        if hdr[cnt] == "Benchmark":
                            testName = text
                        elif hdr[cnt] == "BaseRatio":
                            testScore = text
                    cnt = cnt+1
                    entry = entry.findNextSibling("td")
            
                if testScore == None:
                    print "Missing score for " + testName
                    #raise Exception("Missing score for " + testName)
                
                saveData.update(testName, testScore)

            line = line.findNextSibling("tr")
        
        #pdb.set_trace()

        # store HW attributes
        tab = tab.findNextSibling("table").table
        if tab != None:
            line = tab.tr
            #loop through all lines in table 
            while line:
                if line.td:
                    attr = str(line.th.text)
                    data = str(line.td.text)
                    saveData.update(attr,data) 

                # go to next line
                line = line.findNextSibling("tr")

        else:
            error = True

        return error

