import re

class SpecMachine:
    "A class to aid in parsing spec machines, which can be in a number of forms"
    def __init__(self, string):
        # init our self variables
        self.__hw    = "NA"
        self.__proc  = "NA"
        self.__clock = "NA"

        # we compile this once here for efficiency
        self.__reClkStr = re.compile("(\d+\.?\d*)\s*([MmGg][Hh][Zz])")

        fullTokens = list()

        # first parse the string into parenthesized tokens
        tokens = re.split(r'[()]', string)

        # now for each token, split by commas
        for token in tokens:
            tmp = token.split(",")
            fullTokens.extend(tmp)
        
        # now iterate over the tokens, looking for matches
        taken = list()
        for token in fullTokens:
            if self.__setProc__(token) or self.__setClock__(token):
                taken.append(token)

        # remove taken tokens
        for token in taken:
            fullTokens.remove(token)

        self.__hw = str.join(" ", fullTokens).strip()


    def hw(self):
        return self.__hw

    def proc(self):
        ret = self.__proc
        if (not self.__isProcSet__()) and self.__isClockSet__():
            ret = self.clock()
        return ret

    def clock(self):
        return self.__clock

    def __isProcSet__(self):
        return self.__proc != "NA"

    def __isClockSet__(self):
        return self.__clock != "NA"


    def __setProc__(self, token):
        ret = False
        if not self.__isProcSet__():
            if (token.lower().find("xeon")     >= 0 or
                token.lower().find("celeron")  >= 0 or
                token.lower().find("core 2")   >= 0 or
                token.lower().find("core i3")  >= 0 or
                token.lower().find("core i5")  >= 0 or
                token.lower().find("core i7")  >= 0 or
                token.lower().find("core duo") >= 0 or
                token.lower().find("opteron")  >= 0 or
                token.lower().find("athlon")   >= 0 or
                token.lower().find("phenom")   >= 0 or
                token.lower().find("pentium")  >= 0):
                self.__proc = token.strip()
                ret = True
        return ret


    def __setClock__(self, token):
        ret = False
        if not self.__isClockSet__():
            match = self.__reClkStr.search(token)
            if match:
                #self.__clock = token
                self.__clock = int(match.group(1).strip())
                if match.group(2).lower() == "ghz":
                    self.__clock *= 1000
                #self.__clock = match.group(1).strip()
                ret = True
        return ret
