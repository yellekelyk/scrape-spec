from ordereddict import OrderedDict
import SpecDataElem

class SpecDataBase:
    "A Base class for parsing Spec tables"
    def __init__(self, soup, elem=SpecDataElem):
        self.__elem = elem
        tabs = self.htmlTables(soup)
        self.__tables = OrderedDict()
        for tab in tabs:
            table = self.parseTable(tab)
            if table.name() not in self.__tables:
                self.__tables[table.name()] = table
            else:
                raise Exception("Table " + table.name() + " duplicated!")

    def getElem(self):
        return self.__elem

    def htmlTables(self, soup):
        raise Exception("htmlTables() must be redefined!")

    def getNames(self):
        return self.__tables.keys()

    def getTable(self, name):
        return self.__tables[name]

    def parseTable(self, tab):
        raise Exception("parseTable() must be redefined!")
         

    def numTables(self):
        return(len(self.__tables))

    def toString(self, name):
        return self.__tables[name].toString()

