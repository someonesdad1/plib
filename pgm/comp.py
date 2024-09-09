'''
Search for text in the components database
'''
if 1:   # Header
    if 1:   # Imports
        import sys
        import os
        import getopt
        import csv
        import re
        from collections import defaultdict
        from pdb import set_trace as xx
        from functools import cmp_to_key
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import dedent
        from columnize import Columnize
        from color import TRM as t
    if 1:   # Global variables
        beginning_lines_to_ignore = 3
        data_file = "/elec/spreadsheets/Components.csv"
        # Colors
        t.hl = t("yel")         # Highlight for a regexp
        t.cat = t("lill")       # Highlight for category
        t.warn = t("ornl")      # Color for a missing category warning
        t.N = t.n
if 1:   # Classes
    class Entry:
        def __init__(self, line_number, item):
            self.line_number = line_number
            self.box = item[0]
            self.compartment = item[1]
            self.loc = ':'.join(item[0:2])
            self.descr = item[2]
            kw = ' '.join(item[3:])
            kw = kw.replace(",", " ")
            self.kw = kw.split()
            # Print out the item to stderr if there's no keyword
            if not kw.strip() and item[0]:
                t.print(f"{t.warn}Missing keyword in line {line_number}:  {item!r}", file=sys.stderr)
        def __str__(self):
            s = '/'.join(self.kw)
            if d["-c"]:
                return f"{self.loc} {self.descr} {t.cat}{s}{t.n}"
            else:
                return f"{self.loc} {self.descr}"
if 1:   # Utility
    def Usage(status=0):
        print(dedent(f'''
            {sys.argv[0]} [options] [regex [regex2...]]
              Searches the components database for the indicated regular expressions OR'd
              together.  The search is case-insensitive.  The data file is 
                {data_file!r}
            Options
              -a        Dump all records
              -b N      Show contents of box number N
              -C        Turn off color highlighting
              -c        Show category
              -k kwd    Show items with keyword kwd
              -l        List the keywords
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Dump all records
        d["-b"] = None      # Specifies box number to list
        d["-C"] = True      # Use color highlighting
        d["-c"] = False     # Show category
        d["-k"] = ""        # Show this keyword
        d["-l"] = False     # List the keywords
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "ab:Cchk:l")
        except getopt.GetoptError as e:
            print(str(e))
            sys.exit(1)
        for o, a in optlist:
            if o[1] in "aCcl":
                d[o] = not d[o]
            elif o in ("-b",):
                d["-b"] = int(a)
            elif o in ("-h",):
                Usage()
            elif o in ("-k",):
                d["-k"] = a
        return args
if 1:   # Core functionality
    def GetData():
        # Return a list of Entry items
        items = []
        C = csv.reader(open(data_file, "r"))
        for i, row in enumerate(C):
            if i < beginning_lines_to_ignore or row[2] == "Empty":
                continue
            entry = Entry(i + 1, row)
            items.append(entry)
        return items
    def strsort(a, b):
        '''Sorting comparison function for lines to be printed.  The line is
        split on whitespace, then the first term is split on the colon.  The
        primary sort key is the first integer (box number) and the second sort
        key is the second integer, the compartment number.
    
        Example:  two incoming lines are:
            '2:7      LED, amber, 3 mm'
            '2:16     LED bars'
        Then
            a1, a2 = 2, 7
            b1, b2 = 2, 16
        Since a1 == b1, we have a2 < b2, so -1 is returned.
        '''
        a1, a2 = map(int, a.split()[0].split(":"))
        b1, b2 = map(int, b.split()[0].split(":"))
        if a1 < b1:
            return -1
        elif a1 == b1:
            if a2 < b2:
                return -1
            elif a2 == b2:
                return 0
            else:
                return 1
        else:
            return 1
    def TextSearch(args, d, items):
        # found will hold the lines that matched; pos holds the start and
        # end position of the first match and is keyed by the line.
        regexps, found, pos = [], [], {}
        for i in args:
            regexps.append(re.compile(i, re.I))
        for i in items:
            s = str(i)
            for r in regexps:
                mo = r.search(s)
                if mo:
                    pos[s] = (mo.start(), mo.end())
                    found.append(s)
                    break
        found = list(set(found))
        found.sort(key=cmp_to_key(strsort))
        if found:
            for i in found:
                n, m = pos[i]       # Start & end of match
                spc = i.find(" ")   # Location of first space after box/bin
                # If the start or end are less than the location of the
                # space, then don't print this item
                if n < spc or m < spc:
                    continue
                print(i[:n], end="")
                if d["-C"]:
                    print(f"{t.hl}", end="")
                print(i[n:m], end="")
                if d["-C"]:
                    print(f"{t.n}", end="")
                print(i[m:])
        exit(0)
    def Keywords(items):
        'Returns a set of the keywords'
        kw = []
        for i in items:
            kw.extend(i.kw)
        return set(kw)

if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if not d["-C"]:
        t.cat = t.hl = t.N = ""
    items = GetData()
    if d["-a"]:
        # Show all items
        for i in items:
            if str(i) == ": ":
                print()
            else:
                print(i)
        exit(0)
    elif d["-b"] is not None:
        # Show items in box number -b
        n = d["-b"]
        for i in items:
            if str(n) == i.box:
                print(i)
        exit(0)
    elif d["-l"]:
        # Show allowed keywords
        print("Allowed keywords:\n")
        kw = []
        for i in items:
            kw.extend(i.kw)
        for i in Columnize(sorted(Keywords(items), key=str.lower)):
            print(i)
        exit(0)
    elif d["-k"]:
        # Show all the items with the given keyword
        kw = d["-k"].lower()
        for i in items:
            ikw = [j.lower() for j in i.kw]
            if kw in ikw:
                print(i)
        exit(0)
    if not args:
        Usage()
    TextSearch(args, d, items)
