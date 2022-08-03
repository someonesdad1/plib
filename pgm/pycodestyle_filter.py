'''
Filter output of pycodestyle to a more compact representation
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Filter output of pycodestyle to a more compact representation
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from get import GetLines
        from wrap import wrap, dedent
        from lwtest import Assert
        from color import Color, TRM as t
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Include column numbers
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ch", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def ProcessLines(lines):
        'Return a dict of the lines keyed by error/warning number'
        di = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            f = line.split(":")
            Assert(len(f) in (4, 5))
            file = f[0]
            if d["-c"]:
                linenum = f"{int(f[1])}:{int(f[2])}"
            else:
                linenum = f"{int(f[1])}"
            # Get error/warning and description
            g = ''.join(f[3:]).strip().split()
            errn = g[0]
            descr = ' '.join(g[1:]).strip()
            if 1:
                print(file, linenum, errn, repr(descr))

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if files == ["-"]:
        lines = GetLines(sys.stdin)
    else:
        lines = []
        for file in files:
            lns = GetLines(file)
            lines.extend(lns)
    if 0:
        for i in lines:
            print(i)
    di = ProcessLines(lines)
