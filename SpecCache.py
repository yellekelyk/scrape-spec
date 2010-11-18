import re
class SpecCache:
    "A class to aid in parsing spec caches, which can be in a number of forms"
    def __init__(self, string):
        self.__string = string

        #now remove all matched tokens to leave the description
        #description = re.sub(pat, '', string.lower())
        description = string
        tokens = re.split("D\s*\)?", string)
        if len(tokens) == 2:
            description = tokens[1].lstrip(" ")

        self.__desc = description

    def matches(self, pat="(\d+)\s*([kmg]b)\s*(i|d|i\s*\+\s*d)"):
        matches = re.findall(pat, self.__string.lower())
        #if len(matches) == 0:
        #    raise Exception("Bad input to SpecCache: " + self.__string)
        return matches

    def description(self):
        return self.__desc


    def toKB(self, sizeStr):
        mult = 1
        check = re.search("([kmg]b)", sizeStr.lower())
        if check:
            if check.group(1) == "kb":
                pass
            elif check.group(1) == "mb":
                mult = 1024
            elif check.group(1) == "gb":
                mult = 1024 * 1024
            else:
                raise Exception("Unexpected string " + sizeStr)
        return mult
