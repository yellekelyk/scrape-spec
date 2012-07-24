from SpecDataBase import *
import SpecDataElem
import Table
from ordereddict import OrderedDict
import pdb
import urllib
import BeautifulSoup


class Spec2006Data(SpecDataBase):
    "A class that parses and holds spec2006 data" 

    def __init__(self, soup, elem=SpecDataElem):
        SpecDataBase.__init__(self,soup,elem=elem)

    def htmlTables(self, soup):
        return soup.findAll(attrs={"class":"idx_table"})


    def parseTable(self, tab):
        table = Table.Table(str(tab.a.text), self.getElem()().attrs())

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
                saveData = self.getElem()()
                #saveData = SpecDataElem.SpecDataElem()
                entry = line.td
                while entry:
                    if entry != '\n': 
                        attr = entry.get("class")
                        data = str(entry.text)
                        if entry.firstText() != None:
                            tmp = entry.firstText()
                            data = str(tmp.previousSibling)

                        data = data.replace('&nbsp;', '')
                        #print attr, data
                        saveData.update(attr,data) 

                        # this is where we get the link to hw_model
                        if attr == "hw_model":
                            link = str("http://www.spec.org/cpu2006/results/" + 
                                       str(entry.a['href']))
                            html = urllib.urlopen(link).read()
                            saveData.update("link", link)
                            soup = BeautifulSoup.BeautifulSoup(html)
                            self.__parseDetails__(saveData, soup)
                            
                    entry = entry.nextSibling
                table.addEntry(saveData)

            # go to next line
            line = line.findNextSibling("tr")
        
        return table

    def __parseDetails__(self, saveData, soup):
        
        saveData.update("hw_avail", 
                        str(soup.find(attrs={"id":"hw_avail_val"}).text))

        tab = soup.find(attrs={"id":"Hardware"})
        line = tab.tbody.tr
        #loop through all lines in table 
        while line:
            attr = str(line.th.text)
            data = str(line.td.text)

            saveData.update(attr,data) 

            # go to next line
            line = line.findNextSibling("tr")


        results = soup.find(attrs={"class":"resultstable"})
        line = results.table.tbody.tr
        while line:
            entry = line.td
            if entry.get("class") != "bm":
                raise Exception("Expected class 'bm', got " + 
                                entry.get("class"))
            testName  = str(entry.text).replace('&nbsp;', '')
            testScore = None
            while entry:
                if entry.get("class") == "basecol ratio selected":
                    testScore = str(entry.text).replace('&nbsp;', '')

                entry = entry.findNextSibling("td")
            
            if testScore == None:
                print "Missing score for " + testName
                #raise Exception("Missing score for " + testName)
                
            #pdb.set_trace()
            saveData.update(testName, testScore)

            line = line.findNextSibling("tr")
