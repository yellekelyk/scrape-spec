from SpecDataElem import *
import urllib
import BeautifulSoup


#def getLinks(url):
#    """ give it the url, will extract an array of links to details"""
#    html = urllib.urlopen(url).read()
#    soup = BeautifulSoup.BeautifulSoup(html)
#    
#    line = soup.pre.findNext("a")
#    links = []
#    while line:
#        if str(line.text) == "HTML":
#            link = str("http://www.spec.org" + str(line['href']))
#            links.append(link)
#        line = line.findNext("a")
#    return links



class SpecDataElem1992(SpecDataElem):
    "A class that holds/parses spec92 data for a given processor"
    def __init__(self, tests, attrMap=dict()):
        SpecDataElem.__init__(self, tests=tests)

        # map this table's headers to our standard attrs
        # to do: figure out a more enum-y way to do this
        # especially b.c standard attrs are ugly (include colons)
        self.__attrMap = {"Model Number": "hw_model",
                          "Hardware Availability": "hw_avail",
                          "By": "test_sponsor",
                          "Number of CPUs" : "hw_nchips",
                          "CPU": "CPU:",
                          "Primary Cache" : "Primary Cache:",
                          "Secondary Cache" : "Secondary Cache:",
                          "Other Cache": "L3 Cache:"
                          }
        self.__attrMap.update(attrMap)


    def update(self, attr, data):
        if attr in self.__attrMap:
            attr = self.__attrMap[attr]
        SpecDataElem.update(self, attr, data)

