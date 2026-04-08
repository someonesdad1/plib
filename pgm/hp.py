'''
Open up an HP catalog.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Open up a specified HP catalog
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from columnize import Columnize
        import trm
        t = trm.TrmDP()
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        g.cygstart = "/mnt/d/cygwin64/bin/cygstart.exe"
        g.years = {}  # dict of PDF files indexed by integer year
if 1:  # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] year1 [year2...]
          Open the HP catalog PDF for the indicated year.  If the year doesn't exist, it
          is incremented until a valid year is found.
        Options:
            -h      Print a manpage
            -l      Print first & last years for various HP instrument models
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-l"] = False  # Show first and last years of instrument models
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hl")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("l"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        return args
if 1:  # Show first and last years of various instrument models
    class Inst:
        def __init__(self, model, description, first=None, last=None):
            '''Provide model number as a string and a description.  first and last are integer
            years of introduction and last in the catalog or None if not known
            '''
            self.model = model
            self.desc = description
            self.first = str(first) if first is not None else "?"
            self.last = str(last) if last is not None else "?"
            self.w = (10, 30, 5, 5)
        def __str__(self):
            s = []
            u = f"{self.model:{self.w[0]}s} "
            u += f"{self.desc:{self.w[1]}s} "
            u += f"{self.first:>{self.w[2]}s}-"
            u += f"{self.last:<{self.w[2]}s}"
            s.append(u)
            return "".join(s)
    def ShowModelYears():
        '''Print out information on the first and last years of selected instrument models.  This
        isn't a comprehensive list, but rather those instruments that are of interest to me.
        '''
        models = (
            Inst("400E/EL", "AC voltmeter", 1965, 1986),
            Inst("400F/FL", "AC voltmeter", 1967, 1986),
            Inst("403A", "AC voltmeter", 1960),
            Inst("427A", "Multi-function meter", 1967, 1986),
        )
        for m in models:
            print(m)
if 1:  # Open catalogs
    def GetPDFs():
        "Construct dict mapping year to file"
        dir, g.years = P("/manuals/catalogs/hp"), {}
        for f in dir.glob("*.pdf"):
            name = f.stem
            if "_" in name or "-" in name:
                continue
            if "Agilent" in name:
                i = int(name.replace("Agilent", ""))
            else:
                i = int(name)
            g.years[i] = f
        return g.years
    def GetYear(year):
        '''year is a two or four digit string for a year.  Convert it to a proper
        catalog year and get the first year >= this value that has a valid catalog file.
        '''
        msg = f"{year!r} isn't a valid year"
        try:
            yr = int(year)
        except ValueError:
            Error(msg)
        if yr < 0:
            Error(msg)
        elif yr < 100:
            if 50 <= yr < 100:
                yr += 1900
            elif 0 <= yr <= 3:
                yr += 2000
            else:
                Error(msg)
        else:
            if not (1950 <= yr <= 2003):
                Error(msg)
        # Have a suitable value for year.  If it is not in the g.years dictionary,
        # increment it until it is or it's > 2003.
        while yr <= 2003:
            if yr in g.years:
                return yr
            yr += 1
        Error(msg)
    def GetFile(args):
        "args is a list of 0 or more arguments.  Return a list of the PDFs to open."
        files = []
        if not args:
            return []
        for year in args:
            yr = GetYear(year)
            file = g.years[yr]
            if file not in files:
                files.append(file)
        return files
    def ShowYears():
        'Print the catalog years that are valid'
        print("The following are the HP catalog years (invalid years are gray):")
        yrs = []
        for year in range(1950, 2004):
            if year in g.years:
                yrs.append(f"{t.whtl}{year}{t.n}")
            else:
                yrs.append(f"{t.gryd}{year}{t.n}")
        for i in Columnize(yrs, columns=5, col_width=10, indent=" " * 4):
            print(i)
        print("You can use 2 digit or 4 digit years.  If you give an invalid year,")
        print("the next valid year's catalog will be opened.")
        exit(0)
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    g.years = GetPDFs()
    if d["-l"]:
        ShowModelYears()
    else:
        if not args:
            ShowYears()
        files = GetFile(args)
        for file in files:
            subprocess.run([g.cygstart, file])
