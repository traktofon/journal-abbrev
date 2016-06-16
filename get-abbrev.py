#!/usr/bin/env python3

import requests
from lxml import etree
from io import StringIO

url = "http://adsabs.harvard.edu/abs_doc/journals2.html"

def pairwise(it):
    a = iter(it)
    return zip(a,a)

r = requests.get(url)
assert (r.status_code == 200)

p = etree.HTMLParser()
t = etree.parse( StringIO(r.text), p )
b = t.find("body")
c = b.find("pre")

i = c.itertext()
x = next(i) # skip one
for x,y in pairwise(i):
    abbr = x.strip()
    journal = y.strip()
    print("%s = %s" % (abbr,journal))

