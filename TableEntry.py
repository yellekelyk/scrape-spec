from odict import OrderedDict

class TableEntry:
    "A generic class that holds table-based data"
    def __init__(self, attrs):
        self.__data  = OrderedDict()
        for attr in attrs:
            self.__data[attr] = None

    def attrs(self): 
        return self.__data.keys()

    def update(self, attr, data):
        if attr in self.__data:
            if self.__data[attr] != None:
                raise Exception("Already updated attribute:" + attr)
            self.__data[attr] = data
        else:
            pass 
        #raise Exception(str("Bad attribute:" + attr))

    def get(self, attr):
        if attr not in self.__attrs:
            raise Exception(str("Bad attribute:" + attr))
        return self.__data[attr]


    def toString(self):
        ret = str()
        tmp = self.attrs()
        ret += str(self.__data[tmp[0]]).replace(",", ";")
        for idx in range(1, len(tmp)):
            ret += str("," + str(self.__data[tmp[idx]]).replace(",",";"))
        ret += "\n"
        return ret
