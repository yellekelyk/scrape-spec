from TableEntry import * 

class Table:
    "A class that holds a table of data"
    def __init__(self, name, hdr):
        self.__name = name
        self.__hdr = hdr
        self.__data = list()

    def name(self):
        return self.__name

    def addEntry(self, entry):
        if set(entry.attrs()) ^ set(self.__hdr) != set():
            raise Exception("Attempt to add entry with attrs:" + str(entry.attrs()) + ", expected " + str(self.__hdr))
        self.__data.append(entry)

    def toString(self):
        ret = str()
        tmp = list(self.__hdr)
        ret += str(tmp[0])
        for idx in range(1, len(tmp)):
            ret += str("," + tmp[idx])
        ret += "\n"
        for entry in self.__data:
            ret += entry.toString()
        return ret
        
    def rows(self):
        return len(self.__data)
