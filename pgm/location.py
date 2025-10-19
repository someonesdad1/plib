_pgminfo = '''
<oo desc
    Change (lat,long) location references to gfm links to Google maps.
    Example:  🟨Description (lat,long)🟨 will become [Description](X) where
    X is 'https://www.google.com/maps/search/?api=1&query=latitude,longitude',
    a Google map URL to that location.  Reads lines from stdin and sends the modified
    lines to stdout.
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo

    - List of todo items here

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
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
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Turn 🟨Description (lat,long)🟨 into gfm links to Google maps.  All file input
          is printed to stdout.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def ProcessLine(line):
        '''Example:  🟨Description (lat,long)🟨 will become [Description](X) where
        X is 'https://www.google.com/maps/search/?api=1&query=latitude,longitude',
        a Google map URL to that location.
        '''
        mo = g.r.search(line)
        if not mo:
            print(line)
            return
        des, lat, lon = mo.groups()
        des = des.strip()
        if None in (des, lat, lon):
            print(line)
            return
        # Have a match
        a, b = mo.span()
        start, end = line[:a], line[b:]
        s = "https://www.google.com/maps/search/?api=1&query="
        new_line = f"{start} [{des}]({s}{lat},{lon}) {end}"
        print(new_line)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    # regex to extract components of a location URL
    g.r = re.compile(r'''
        🟨\ *                       # Starting trigger string
        (?P<des>[^(]*)              # Description
        \(                          # Beginning parenthesis
        (?P<lat>[+-]?\d+\.\d+)      # Latitude
        , *                         # Comma
        (?P<lon>[+-]?\d+\.\d+)      # Longitude
        \)                          # Ending parenthesis
        \ *🟨                       # Ending trigger string
    ''', re.X)
    for file in files:
        lines = open(file).readlines()
        for line in lines:
            line = line.rstrip("\n")    # Remove newline
            ProcessLine(line)
