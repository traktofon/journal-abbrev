journal-abbrev
==============

This is a set of small scripts for converting BibTeX files to use
journal abbreviations, which are required by some scientific
publishers.  Additionally some unnecessary fields can be removed
from the BibTeX entries, in order to reduce filesize.

My use case is that the BibTeX export from [Zotero](https://www.zotero.org/)
often contains the full journal name.  While there is an option to "use
journal abbreviations", this only has an effect if the Zotero entry contains
a proper "Journal Abbr" field.  But in my workflow, this field is normally
not populated, and I can't be bothered to add it manually.  Additionally,
different publishers may require different styles of abbreviation.  

There are currently two scripts:
1. **get-abbrev.py** downloads a list of journal abbreviations, currently
   from the [ADS service](http://adsabs.harvard.edu/abs_doc/journals2.html)
   and saves it in a simple text file, which can be edited or amended.
2. **bibtex-abbrev.py** takes a BibTeX file and the abbreviation definitions
   produced by **get-abbrev.py**, replaces (as far as possible) full journal
   names by their abbreviations, removes unnecessary fields from the
   BibTeX entries, and writes out a new BibTeX file.


Prerequisites
-------------

You need to have Python3 installed. This was tested with Python version 3.4.3.

**get-abbrev.py** requires the Python modules *requests* and *lxml*.
On Debian/Ubuntu, you can install them with:
```
sudo apt-get install python3-requests python3-lxml
```

**bibtex-abbrev.py** requires the Python module *bibtexparser*.
It can be installed with:
```
pip install --user bibtexparser
```
or whatever way you prefer to manually install Python modules.


Usage
-----

**get-abbrev.py** currently only supports the abbreviation definitions
from the [ADS service](http://adsabs.harvard.edu/abs_doc/journals2.html).
It attempts to parse the abbreviation definitions from their web page,
and dumps them to standard output in a simple text format, which is
easy to edit and to which you can add your own definitions. Run it as:
```
python3 get-abbrev.py > abbrev.txt
```
The output file format is very simple, namely it consists of lines of
the form
```
JwvlT = The Journal with a very long Title
```
That is, abbreviation and full title are separated by an equals sign.

**bibtex-abbrev.py** takes the names of a BibTeX file and the abbreviation
definition file, replaces full journal names with the corresponding
abbreviation, and writes the modified file to standard output. Example:
```
python3 bibtex-abbrev.py orig.bib abbrev.txt > new.bib
```
If additionally the option *-m* or *--minify* is given, the program will
also remove some fields from the BibTeX entries, i.e. fields which are specific
to Zotero or which are not needed for citations in science journals.
Currently the removed fields are:
- abstract
- keyword
- file
- link


TODO
----

The following features may be implemented when the need arises:
* Get abbreviation definitions from other sources.
* Fuzzily match journal names from BibTeX with those from the definitions.

