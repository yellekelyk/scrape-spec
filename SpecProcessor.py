import re
import pdb
from odict import OrderedDict

class SpecProcessor:
    "A class to aid in parsing spec processors, which can be in a number of forms"
    def __init__(self, string):
        # init our self variables
        self.__make    = "NA"
        self.__family  = "NA"
        self.__model   = "NA"
        self.__misc    = "NA"
        self.__bus     = "NA"
        self.__clk     = "NA"

        self.__makeFamily = {"AMD" : ["Athlon 64 X2", 
                                      "Athlon 64", 
                                      "Athlon Thunderbird",
                                      "Athlon XP",
                                      "Athlon",
                                      "Opteron",
                                      "Phenom II X3",
                                      "Phenom II X4",
                                      "Phenom X3",
                                      "Phenom X4",
                                      "Turion 64 X2"],

                             "DEC" : ["Alpha", 
                                      "21064A",
                                      "21064",
                                      "21164A", 
                                      "21164", 
                                      "21264A", 
                                      "21264"],
                             "Fujitsu" : ["SPARC64 GP",
                                          "TurboSPARC"],
                             "HAL" : ["SPARC64"],
                             "HP" : ["PA-8700+",
                                     "PA-8700",
                                     "PA-8000",
                                     "PA-7300",
                                     "PA-7200",
                                     "PA-7150",
                                     "PA-7100",
                                     "PA-7000",
                                     "PA-8600",
                                     "PA-8500",
                                     "PA-8200"],
                             "IBM" : ["RS64-III",
                                      "RS64-II",
                                      "RS64 IV",
                                      "Power2",
                                      "Power3-II",
                                      "Power3",
                                      "Power6",
                                      "Power5",
                                      "Power7",
                                      "PowerPC"],
                             "Intel" : ["Atom",
                                        "Celeron",
                                        "Core 2 Duo",
                                        "Core 2 Extreme",
                                        "Core 2 Quad",
                                        "Core 2 Solo",
                                        "Core Duo",
                                        "Core i3",
                                        "Core i5",
                                        "Core i7",
                                        "Itanium 2",
                                        "Itanium",
                                        "Pentium 4 EE",
                                        "Pentium 4",
                                        "Pentium D",
                                        "Pentium EE",
                                        "Pentium III",
                                        "Pentium II",
                                        "Pentium MMX",
                                        "Pentium M",
                                        "Pentium Pro",
                                        "Pentium",
                                        "Xeon"],
                             "MIPS" : ["R14000A",
                                       "R14000",
                                       "R12000A",
                                       "R12000",
                                       "R10000",
                                       "R8010",
                                       "R8000",
                                       "R5000",
                                       "R4600",
                                       "R4400",
                                       "R3000",
                                       "R2000"],
                             "Ross" : ["HyperSPARC"],
                             "Sun" : ["SuperSPARC II",
                                      "SuperSPARC", 
                                      "UltraSPARC III",
                                      "UltraSPARC IIi",
                                      "UltraSPARC II",
                                      "UltraSPARC",
                                      "MicroSPARC II"]}

        # now invert!
        # use OrderedDict to preserve implicit orderings
        self.__familyMake = OrderedDict()
        for make in self.__makeFamily:
            for family in self.__makeFamily[make]:
                if family in self.__familyMake:
                    raise Exception("Family " + family + " is duplicated")
                self.__familyMake[family] = make
       
        self.__allMakes = self.__makeFamily.keys()
        self.__allFamilies = self.__familyMake.keys()

        # use this to preprocess the string (hard-coded common cases)
        self.__preprocess = [("PA-RISC", "PA"),
                             ("PA\s*(\d\d\d\d)", "PA-\\1"),
                             ("SPARC-I", "SPARC I"),
                             ("\s*\(\s*TM\s*\)\s*", " "),
                             ("\s*[Pp]rocessor\s*", " ")]

        for regex in self.__preprocess:
            string = re.sub(regex[0], regex[1], string)


        #string = re.sub("\s*\(\s*TM\s*\)\s*", " ", string)
        # remove '(TM)' string (it's fairly common)
        
        # now iterate over the tokens, looking for matches
        #taken = list()
        #for token in fullTokens:
        string2 = self.__setMake__(string) 
        string3 = self.__setFamily__(string2)
        self.__misc  = string.strip()

        self.__setBus__(self.__misc)
        if self.__bus == "NA":
            self.__setClock__(self.__misc)

        # hard-coded pathological fix for SPARC IIi and SPARC III
        if self.__family == "UltraSPARC III":
            if re.search("IIi", self.__misc):
                self.__family = "UltraSPARC IIi"


        # verify family/make!
        if self.__make == "NA":
            if self.__family == "NA":
                pass
            else:
                self.__make = self.__familyMake[self.__family]
        elif self.__family == "NA":
            self.__family = self.__makeFamily[self.__make]
        elif not self.__family in self.__makeFamily[self.__make]:
            raise Exception(str("family " + self.__family + 
                                "doesn't match family for make=" + self.__make))

        # attempt to set model name given family, clock, etc
        string4 = self.__setModel__(string3)


    def make(self):
        return self.__make

    def family(self):
        return self.__family

    def model(self):
        return self.__model

    def misc(self):
        return self.__misc

    def bus(self):
        return self.__bus

    def clk(self):
        return self.__clk

    def __isMakeSet__(self):
        return self.__make != "NA"

    def __isFamilySet__(self):
        return self.__family != "NA"
    
    def __setMake__(self, token):
        (self.__make, token) = self.__findAndRemoveFirst__(self.__allMakes, token)
        return token

    def __setFamily__(self, token):
        (self.__family, token) = self.__findAndRemoveFirst__(self.__allFamilies, token)
        #if re.search("SPARC", self.__family)

        return token


    def __setModel__(self, token):

        # remove any clock business
        token = re.sub("\d+\.?\d*\s*[MmGg][Hh]z", "", token)

        # remove any parentheses
        token = token.replace("(","")
        token = token.replace(")","")

        # remove any outer spaces
        token = token.strip()

        # if we're blank, use a default model name!
        if token == "":
            self.__model = self.__family + ":" + self.__clk
        else:
            self.__model = token

        return token

    def __setBus__(self, token):
        m = re.search("(\d+\.?\d*)\s*([MmGg][Hh][Zz])\s*(system)?\s*(bus|fsb)", token, re.IGNORECASE)
        if m:
            bus = m.group(1)
            units = m.group(2)
            if re.search("ghz", units, re.IGNORECASE):
                bus = bus * 1000
            self.__bus = bus

    def __setClock__(self, token):
        m = re.search("(\d+\.?\d*)\s*([MmGg][Hh][Zz])", token, re.IGNORECASE)
        if m:
            clk = float(m.group(1))
            units = m.group(2)
            if re.search("ghz", units, re.IGNORECASE):
                clk = clk * 1000
            self.__clk = str(int(clk))


    def __findAndRemoveFirst__(self, tokens, string, reOpts=re.IGNORECASE):
        #string = stringIn.lower()
        found = "NA"
        for token in tokens:
            regex = re.compile("\s*" + token + "\s*", reOpts)
            m = regex.search(string)
            if m:
                found = token
                string = regex.sub(" ", string)
                break
        return (found, string)
