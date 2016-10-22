#!/usr/bin/env python3

import bibtexparser as bp
import argparse
import re


def fix_journal(j):
    "Attempt to canonicalize the journal name."
    j = j.lower()
    j = j.replace("," , ""   )
    j = j.replace("\&", "and")
    j = re.sub(" *the *", " ", j).strip()
    return j


def fix_abbrev(a):
    "Encode the abbreviation string for LaTeX."
    a = a.replace("&", "\&")
    return a


def parse_abbrev(fnam):
    "Reads abbreviation database from file _fnam_ and returns it as a dictionary."
    with open(fnam) as af:
        als = af.readlines()
    abbdb = {}
    for al in als:
        eqpos = al.find("=")
        if eqpos<0: continue # ignore lines without =
        abbrev = al[:eqpos].strip()
        journal = al[eqpos+1:].strip()
        journal = fix_journal(journal)
        abbdb[journal] = abbrev
    return abbdb


def parse_bibtex(fnam):
    "Reads BibTeX from file _fnam_ and returns it as a BibDatabase."
    with open(fnam) as bf:
        bt = bf.read()
    bibdb = bp.loads(bt)
    return bibdb


def bibtex_abbrev(bibdb, abbdb):
    """
    Substitutes the journal entries in the BibDatabase _bibdb_ with
    abbreviations from the dictionary _abbdb_.
    """
    for entry in bibdb.entries:
        j = entry.get("journal")
        if j is None: continue # skip non-journal entry
        j = fix_journal(j)
        if abbdb.get(j):
            # abbrevation found, so substitute
            entry["journal"] = fix_abbrev(abbdb[j])
    return bibdb


def bibtex_minify(bibdb):
    "Removes unwanted information from the BibTex entries."
    for entry in bibdb.entries:
        for field in [ "abstract", "file", "keyword", "link" ]:
            if entry.get(field): del entry[field]
    return bibdb


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description = "Abbreviate journal names in BibTeX files.",
        epilog = "The modified BibTeX file is written to stdout." )
    ap.add_argument(
        "-m", "--minify",
        action = "store_true", dest = "minify",
        help = "remove some unwanted fields from the BibTeX entries" )
    ap.add_argument(
        "bibfile",
        help = "name of the original BibTeX file")
    ap.add_argument(
        "abbrevfile",
        help = "name of the file containing the abbreviation definitions")
    args = ap.parse_args()

    bibdb = parse_bibtex(args.bibfile)
    abbdb = parse_abbrev(args.abbrevfile)
    bibtex_abbrev( bibdb, abbdb )
    if args.minify:
        bibtex_minify(bibdb)
    bt = bp.dumps(bibdb)
    print(bt)

