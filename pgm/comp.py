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
        if 0:
            import debug             
            debug.SetDebugger()      
    if 1:   # Global variables
        beginning_lines_to_ignore = 3
        data_file = "/elec/spreadsheets/Components.csv"
        # Colors
        t.match = t("brnl", attr="it")
        t.box = t("whtl")
        t.compartment = t("grn")
        t.warn = t("ornl")      # Color for a missing category warning
if 1:   # Classes
    class Entry:
        def __init__(self, line_number, item):
            self.line_number = line_number
            self.box = item[0].strip()
            self.compartment = item[1].strip()
            self.loc = ':'.join(item[0:2])
            self.descr = item[2].strip()
            kw = ' '.join(item[3:]) # Keywords
            kw = kw.replace(",", " ")
            self.kw = kw.split()
            # Attributes to indicate a regex match in the self.descr string
            self.start = None
            self.end = None
            # Print out the item to stderr if there's no keyword
            if not kw.strip() and item[0]:
                t.print(f"{t.warn}Missing keyword in line {line_number}:  {item!r}", file=sys.stderr)
        def __str__(self):
            s = '/'.join(self.kw)
            if d["-c"]:
                return f"{self.loc} {self.descr} {t.cat}{s}{t.n}"
            else:
                return f"{self.loc} {self.descr}"
        def __repr__(self):
            return str(self)
        def __lt__(self, other):
            '''Comparison for sorting.  The primary key is the box number and the secondary key is
            the compartment number.
            '''
            if int(self.box) < int(other.box):
                return True
            elif int(self.box) > int(other.box):
                return False
            else:
                return int(self.compartment) < int(other.compartment)
if 1:   # Utility
    def Usage(status=0):
        print(dedent(f'''
            {sys.argv[0]} [options] [regex [regex2...]]
              Searches the components database for the indicated regular expressions AND'd
              together.  The search is case-insensitive.  The data file is 
                {data_file!r}
            Options
              -a        Dump all records
              -b N      Show contents of box number N
              -C        Do not Use color highlighting
              -c        Show category
              -i        Do not ignore case in searches
              -k kwd    Show items with keyword kwd
              -l        List the keywords
              -o        OR the regexes instead of AND
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Dump all records
        d["-b"] = None      # Specifies box number to list
        d["-C"] = True      # Use color highlighting
        d["-c"] = False     # Show category
        d["-i"] = True      # Ignore case
        d["-k"] = ""        # Show this keyword
        d["-l"] = False     # List the keywords
        d["-o"] = False     # OR the regexes on the command line
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "ab:Cchik:lo")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
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
        items, empty = set(), ["", "", "", "", ""]
        C = csv.reader(open(data_file, "r"))
        for i, row in enumerate(C):
            if i < beginning_lines_to_ignore or row[2] == "Empty":
                continue
            if row != empty:
                entry = Entry(i + 1, row)
                items.add(entry)
        items = list(sorted(items))
        return items
    def TextSearch(args, items):
        '''found will hold the Entry items that matched; pos holds the start and
        end position of the first match and is keyed by the line.

        args        List of regexes to search for
        items       List of Entry instances; when printed, an Entry will result in a string like
                    "1:1 Component pins".
        '''
        if 1:  # regexps is a list of the regular expressions made from args
            regexps = []
            for i in args:
                if d["-i"]:
                    regexps.append(re.compile(i, re.I))
                else:
                    regexps.append(re.compile(i))
        if 1:  # Search all the items (Entry instances) for regex matches in their descr attribute
            found = []  # List containing the Entry instances that had a regex match
            if d["-o"]:  # OR the regexes
                for i in items:
                    s = i.descr
                    for r in regexps:
                        mo = r.search(s)
                        if mo:
                            i.start, i.end = mo.start(), mo.end()
                            found.append(i)
                            break
            else:  # AND the regexes
                for i in items:
                    s = i.descr
                    matched_all = True          # Assume we'll match all
                    # Since this is reversed, the only regex that will be color-coded is the first
                    for r in reversed(regexps):
                        mo = r.search(s)
                        if mo:
                            i.start, i.end = mo.start(), mo.end()
                        else:
                            matched_all = False
                    if matched_all:
                        found.append(i)
        if 1:  # Print results
            for item in sorted(found):
                # Print box and compartment in color
                if d["-C"]:
                    print(f"{t.box}{item.box:>2s}:{t.compartment}{item.compartment:>2s}{t.n}", end="")
                else:
                    print(f"{item.box:>2s}:{item.compartment:>2s}", end="")
                # Print description
                print("", end=" "*4)    # Spacing between box:compartment and string
                s = item.descr
                print(s[:item.start], end="")
                # Print the colorized match
                if d["-C"]:
                    print(f"{t.match}", end="")
                print(s[item.start:item.end], end="")   # Colorize the match
                if d["-C"]:
                    print(f"{t.n}", end="")
                # Print remainder
                print(s[item.end:])
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
    if d["-a"]:  # Show all items
        for i in items:
            if str(i) == ": ":
                print()
            else:
                print(i)
        exit(0)
    elif d["-b"] is not None:  # Show items in box number -b
        n = d["-b"]
        for i in items:
            if str(n) == i.box:
                print(i)
        exit(0)
    elif d["-l"]:  # Show allowed keywords
        print("Allowed keywords:\n")
        kw = []
        for i in items:
            kw.extend(i.kw)
        for i in Columnize(sorted(Keywords(items), key=str.lower)):
            print(i)
        exit(0)
    elif d["-k"]:  # Show all the items with the given keyword
        kw = d["-k"].lower()
        for i in items:
            ikw = [j.lower() for j in i.kw]
            if kw in ikw:
                print(i)
        exit(0)
    if not args:
        Usage()
    TextSearch(args, items)
