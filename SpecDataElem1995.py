from SpecDataElem import *
import urllib
import BeautifulSoup


def getLinks(url):
    """ give it the url, will extract an array of links to details"""
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    
    line = soup.pre.findNext("a")
    links = []
    while line:
        if str(line.text) == "HTML":
            link = str("http://www.spec.org" + str(line['href']))
            links.append(link)
        line = line.findNext("a")
    return links



class SpecDataElem1995(SpecDataElem):
    "A class that holds/parses spec95 data for a given processor"
    def __init__(self, tests, attrMap=dict()):
        SpecDataElem.__init__(self, tests=tests)

        # map this table's headers to our standard attrs
        # to do: figure out a more enum-y way to do this
        # especially b.c standard attrs are ugly (include colons)
        self.__attrMap = {"System": "hw_model",
                          "HW Avail": "hw_avail",
                          "Tested By": "test_sponsor",
                          "# cores" : "hw_ncores",
                          "# chips" : "hw_nchips",
                          "# cores per chip" : "hw_ncoresperchip",
                          "Processor": "CPU:",
                          "1st Cache" : "Primary Cache:",
                          "2nd Cache" : "Secondary Cache:",
                          "Other Cache": "L3 Cache:",
                          "Result": "peakmean",
                          "Baseline": "basemean",
                          }
        self.__attrMap.update(attrMap)


    def update(self, attr, data):
        if attr in self.__attrMap:
            attr = self.__attrMap[attr]
        SpecDataElem.update(self, attr, data)

