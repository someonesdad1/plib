'''
Open up an HP catalog.
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Open up a specified HP catalog
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from columnize import Columnize
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        g.cygstart = "/mnt/d/cygwin64/bin/cygstart.exe"
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
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
          Open the HP catalog PDF for the indicated year.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        return args
if 1:   # Core functionality
    def GetPDFs():
        'Construct dict mapping year to file'
        dir, catalogs = P("/manuals/catalogs/hp"), {}
        for f in dir.glob("*.pdf"):
            name = f.stem
            if "_" in name or "-" in name:
                continue
            if "Agilent" in name:
                i = int(name.replace("Agilent", ""))
            else:
                i = int(name)
            catalogs[i] = f
        return catalogs
    def GetFile(args):
        'args is a list of 0 or more arguments.  Return a list of the PDFs to open.'
        pdfs = GetPDFs()    # dict of PDF files indexed by integer year
        files = []
        if not args:
            return None
        for arg in args:
            # arg can be either a 2 digit or 4 digit number.  If 2, then 1900 is added to it; if
            # no match, then 2000 is added to it.
            try:
                yr = int(arg)
            except ValueError:
                print(f"{arg!r} isn't a valid year")
                continue
            found = False
            for i in (0, 1900, 2000):
                if i + yr in pdfs:
                    files.append(pdfs[i + yr])
                    found = True
                    break
            if not found:
                print(f"{arg!r} isn't a valid year")
        return files
    def ShowYears():
        'Print the catalog years that are valid'
        pdfs = GetPDFs()    # dict of PDF files indexed by integer year
        print("The following are the valid HP catalog years:")
        for i in Columnize(pdfs.keys(), columns=5, col_width=10, indent=" "*4):
            print(i)
        print("You can use 2 digit or 4 digit years")
        exit(0)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        ShowYears()
    files = GetFile(args)
    for file in files:
        if 0:
            subprocess.run([g.cygstart, file])
        else:
            print(file)
