#!/usr/bin/env python3

import dryscrape
import time

url = "http://scieng.library.ubc.ca/coden/"

def pairwise(it):
    a = iter(it)
    return zip(a,a)

# load initial document
s = dryscrape.Session()
s.visit(url)
assert(s.status_code() == 200)

# find the "Browse all" link, and click it
q = s.at_xpath("//a[@id='jaall']")
q.click()
time.sleep(5)

# find the DIV with the results
t = s.document()
for el in t.iter():
    if el.get("id") == "jaresults":
        res = el
        break
else:
    raise RuntimeError("No results found")

# extract text from all TD nodes
tds = [ el.text for el in res.iter() if el.tag=="td" and not el.text is None ]

# produce output
for x,y in pairwise(tds):
    abbr = x.strip()
    journal = y.strip()
    print("%s = %s" % (abbr,journal))

