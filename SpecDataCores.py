import re

class SpecDataCores:
    "A class to aid in parsing of core numbers"
    def __init__(self, string):
        # init our self variables
        self.__coresTotal   = "NA"
        self.__chipsTotal   = "NA"
        self.__coresPerChip = "NA"
        self.__thrdsPerCore = "NA"

        fullTokens = list()

        # now split string into tokens by ','
        tokens = string.split(",")
        
        # now iterate over the tokens, looking for matches
        taken = list()
        for token in tokens:
            if self.__setCoresTotal__(token):
                taken.append(token)
            elif self.__setChipsTotal__(token):
                taken.append(token)
            elif self.__setCoresPerChip__(token):
                taken.append(token)


    def __setCoresTotal__(self, token):
        ret = False
        if self.__coresTotal == "NA":
            check = re.search("(\d+)\s*cores?\s*$", token)
            if check:
                self.__coresTotal = check.group(1).strip()
                ret = True
        return ret

    def __setChipsTotal__(self, token):
        ret = False
        if self.__chipsTotal == "NA":
            check = re.search("(\d+)\s*chips?\s*$", token)
            if check:
                self.__chipsTotal = check.group(1).strip()
                ret = True
        return ret

    def __setCoresPerChip__(self, token):
        ret = False
        if self.__coresPerChip == "NA":
            check = re.search("(\d+)\s*cores?\/chip(.*)$", token)
            if check:
                self.__coresPerChip = check.group(1).strip()
                self.__setThrdsPerCore__(check.group(2).strip())
                ret = True

        return ret

    def __setThrdsPerCore__(self, token):
        if self.__thrdsPerCore == "NA":
            if (token.lower().find("disable") >= 0 or
                token.lower().find("off") >= 0):
                self.__thrdsPerCore = "1"
            elif (token.lower().find("enable") >= 0 or
                  token.lower().find("on") >= 0):
                self.__thrdsPerCore = "2"
        

    def coresPerChip(self):
        return self.__coresPerChip

    def thrdsPerCore(self):
        return self.__thrdsPerCore

    def chipsTotal(self):
        return self.__chipsTotal

    def coresTotal(self):
        return self.__coresTotal
