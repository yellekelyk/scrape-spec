from SpecDataBase import *
import SpecDataElem
import Table
from ordereddict import OrderedDict
import re
import urllib
import BeautifulSoup
import utils
import pdb

class Spec1995Data(SpecDataBase):
    "A class that parses and holds spec1995 data" 
    def __init__(self, soup, elem=SpecDataElem):
        self.__hdrMap = {'Tested By:' : 'test_sponsor',
                         'System'  : 'hw_model',
                         '# CPU'   : 'hw_nthreadspercore',
                         'Baseline': 'basemean',
                         'Result'  : 'peakmean',
                         'Disclosure' : 'link'}
        SpecDataBase.__init__(self, soup, elem=elem)

    def htmlTables(self, soup):
        tabs = soup.findAll("h3")
        return tabs


    def parseTable(self, tab):
        name = str(tab.text)
        table = Table.Table(str(tab.text), self.getElem()().attrs())

        line = tab.findNext("pre").findNext("a")

        linecnt = 0

        while line:
            saveData = self.getElem()()
            error = False

            if str(line.text) == "HTML":
                link = str("http://www.spec.org" + str(line['href']))
                print "found link=" + link                
                html = urllib.urlopen(link).read()
                soup = BeautifulSoup.BeautifulSoup(html)
                saveData.update("link", link)
                error = error or self.__parseDetails__(saveData, soup)
                linecnt += 1
            
                if error:
                    print "Warning: skipping line due to error"
                else:
                    table.addEntry(saveData)

            line = line.findNext("a")

            #if linecnt >= 10:
            #    break

        return table



    def __parseDetails__(self, saveData, soup):

        error = False

        #pdb.set_trace()
        ## extract results summary
        #summary = soup.table.tr
        #info = summary.tr.th
        #while info:
            



        perf = soup.table.findNext("table")
        hdrInfo = perf.tr.th
        hdr = list()
        while hdrInfo:
            hdr.append(str(hdrInfo.text))
            hdrInfo = hdrInfo.findNextSibling("th")


        # parse results table
        # todo: this code is nearly identical to code in Spec2000Data
        # consider factoring it to base class
        line = perf.findNext("tr").findNextSibling("tr")
        while line:
            cnt = 0
            entry = line.td

            #we only proceed if there is clearly enough data present
            # (otherwise we might misplace something due to the cnt scheme)
            if len(line.findAll("td")) >= len(hdr):
                testName = None
                testScore = None
                while entry:
                    text = str(entry.text).replace('&nbsp;', '')
                    if cnt < len(hdr):
                        if hdr[cnt] == "Benchmark # and Name":
                            testName = text
                        elif hdr[cnt] == "Base SPEC Ratio":
                            testScore = text
                    cnt = cnt+1
                    entry = entry.findNextSibling("td")
            
                if testScore == None:
                    print "Missing score for " + testName
                
                saveData.update(testName, testScore)

            # check if it's a summary line
            elif len(line.findAll("td")) == 2:
                testName = str(line.td.text)
                if testName == '':
                    testName = str(line.td.findNext("td").text)
                testScore = str(line.th.text)
                saveData.update(testName, testScore)


            line = line.findNextSibling("tr")


        # store Tester info
        perf = perf.findNext("table")
        error = error or self.__parseHTMLTableByRow__(saveData, perf)

        # store HW attributes
        perf = perf.findNext("table")
        error = error or self.__parseHTMLTableByRow__(saveData, perf)

        return error


    def __parseHTMLTableByRow__(self, saveData, table):
        """ Parses an HTML table, assuming each row has `header: value' """
        error = False
        if table:
            line = table.tr
            # loop through all lines in table
            while line:
                if line.td:
                    attr = str(filter(utils.onlyascii, line.th.text))
                    data = str(filter(utils.onlyascii, line.td.text))
                    saveData.update(attr, data)
                line = line.findNextSibling("tr")
        else:
            error = True

        return error


