from odict import OrderedDict

class SpecDataBase:
    "A Base class for parsing Spec tables"
    def __init__(self, soup):
        tabs = self.htmlTables(soup)
        self.__tables = OrderedDict()
        for tab in tabs:
            table = self.parseTable(tab)
            if table.name() not in self.__tables:
                self.__tables[table.name()] = table
            else:
                raise Exception("Table " + table.name() + " duplicated!")

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

