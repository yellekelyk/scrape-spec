import BeautifulSoup
import Spec2006Data
import Spec2000Data
import Spec1995Data
import SpecDataElem
import urllib
import sys
import pdb

def onlyascii(char):
    if ord(char) > 127: return""
    else: return char

def main():

    if len(sys.argv) < 4:
        print "Usage: scrapeSpec url SpecData SpecDataElem\n"
        sys.exit(0)


    html = urllib.urlopen(sys.argv[1]).read()
    html = filter(onlyascii, html)

    #f = open("./test.cint2000.html")
    #html = f.read()
    #f.close()

    soup = BeautifulSoup.BeautifulSoup(html)  
    mod  = __import__(sys.argv[3])
    elem = mod.__dict__.get(mod.__name__)

    mod  = __import__(sys.argv[2])
    data = mod.__dict__.get(mod.__name__)(soup, elem=elem)
    for name in data.getNames():
        f = open(str("./test."+ name.replace(" ", "_").replace(":","") + ".csv"), 
             'w')
        f.write(data.getTable(name).toString())
        f.close()


if __name__ == "__main__":
    main()
