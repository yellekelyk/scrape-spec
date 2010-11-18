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

    f = open("./test.cfp2006.html")
    #f = open("./test2006.small.html")
    html = f.read()
    f.close()

    #html = urllib.urlopen("http://www.spec.org/cpu2000/results/cint2000.html").read()


    html = filter(onlyascii, html)

    soup = BeautifulSoup.BeautifulSoup(html)
    
    elem = SpecDataElem.__dict__.get("SpecDataElem")
    if len(sys.argv) > 1:
        mod  = __import__(sys.argv[1])
        elem = mod.__dict__.get(mod.__name__)

    #data = Spec2000Data.Spec2000Data(soup)
    data = Spec2006Data.Spec2006Data(soup, elem=elem)

#
#for name in data.getNames():
#    f = open(str("./test."+ name.replace(" ", "_").replace(":","") + ".csv"), 
#             'w')
#    f.write(data.getTable(name).toString())
#    f.close()

    #pdb.set_trace()

    for name in data.getNames():
        print data.getTable(name).toString()

if __name__ == "__main__":
    main()
