import BeautifulSoup
import Spec2006Data
import Spec2000Data
import Spec1995Data
import urllib

f = open("./test2000.html")
html = f.read()
f.close()

html = urllib.urlopen("http://www.spec.org/cpu2000/results/cint2000.html").read()


def onlyascii(char):
    if ord(char) > 127: return""
    else: return char

html = filter(onlyascii, html)

soup = BeautifulSoup.BeautifulSoup(html)

data = Spec2000Data.Spec2000Data(soup)
#data = Spec2006Data.Spec2006Data(soup)

for name in data.getNames():
    f = open(str("./test."+ name.replace(" ", "_").replace(":","") + ".csv"), 
             'w')
    f.write(data.getTable(name).toString())
    f.close()


