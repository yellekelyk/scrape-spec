from ordereddict import OrderedDict

class TableEntry:
    "A generic class that holds table-based data"
    def __init__(self, attrs):
        self.__data  = OrderedDict()
        for attr in attrs:
            self.__data[attr] = None

    def attrs(self): 
        return self.__data.keys()

    def update(self, attr, data, allowDup=False):
        if attr in self.__data:
            if self.__data[attr] != None:
                if allowDup:
                    if self.__data[attr] != data:
                        pass
                    #print str("Possible duplicate, exists=" 
                    #+ self.__data[attr] + 
                    #" , new=" + data)
                else:
                    raise Exception("Already updated attribute:" + attr)
            #print attr, data
            self.__data[attr] = data
        else:
            pass
        #print "Skipping attr " + attr
        #raise Exception(str("Bad attribute:" + attr))

    def get(self, attr):
        if attr not in self.attrs():
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
