'''
Input is 'history'; print out the most-used commands.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print most used commands from shell history
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from pathlib import Path as P
        from collections import defaultdict, deque
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from color import t
        from get import GetLines
        from wrap import dedent
        from f import flt
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from wsl import wsl     # wsl is True when running under WSL Linux
        if 1:
            import debug
            debug.SetDebugger()
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stderr   # Debug printing to stderr by default
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file]
          file contains a shell history of commands (or use - to get it
          from stdin).  Print out the most-used commands.
        Options:
            -h      Print a manpage
            -n n    Print out n most-used commands
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-n"] = 20        # Number of commands to print
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "hn:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if d[o] < 1:
                        raise ValueError()
                except ValueError:
                    Error("-n option's argument must be an integer > 0")
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return files
if 1:   # Core functionality
    def ProcessFile(file, di):
        '''file is the file to read (or "-" for stdin).  di is the
        defaultdict(int) to put the command counts in.
        '''
        where = file if file != "-" else sys.stdin
        dq = deque(GetLines(where, nonl=True))
        while dq:
            s = dq.popleft()
            s = s.strip()
            if not s:
                continue
            try:
                _, cmdline = s.strip().split(" ", 1)
            except ValueError:
                # An occasion line will have no command
                continue
            cmd = cmdline.split(" ", 1)[1]
            c = cmd.split()[0]
            c = c.split(";")[0]
            if c.startswith("#"):
                continue
            di[c] += 1
    def Report(di):
        o = list(di.items())
        # Reverse so count is first so sorting is easy
        o = sorted([j, i] for i, j in o)
        # Get the most-used items
        top = list(reversed(o[-d["-n"]:]))
        # Get the total number of commands in history
        N = sum(i for i, j in o)
        # Get the total number of commands in top
        n = sum(i for i, j in top)
        # Construct output list
        dq, out = deque(top), []
        while dq:
            count, cmd = dq.popleft()
            out.append((count, flt(count/N*100), cmd))
        # Get max widths of columns
        w0 = max(len(str(i)) for i, j, k in out)
        w1 = max(len(str(j)) for i, j, k in out)
        # Print header
        h0, h1, h2 = "Count", "% of N", "Command"
        w0 = max(w0, len(h0))
        w1 = max(w1, len(h1))
        s = " "*4
        print(f"{h0:>{w0}s}{s}{h1:>{w1}s}{s}{h2}")
        print(f"{'-'*w0:>{w0}s}{s}{'-'*w1:>{w1}s}{s}{'-'*7}")
        for i in out:
            count, pct, cmd = i
            print(f"{str(count):>{w0}s}{s}{str(pct):>{w1}s}{s}{cmd}")
        print(f"{'-'*w0}{s}{'-'*w1}")
        print(f"{n:{w0}d}{s}{str(flt(100*n/N)) + '%':>{w1}s}")
        print()
        fmt = ">10d"
        print(f"Total of these commands          {n:{fmt}}")
        print(f"Total of all commands in history {N:{fmt}}")
        print(f"These top {d['-n']} commands are {int(100*n/N)}% of the {N} commands in history")

if __name__ == "__main__":
    d = {}      # Options dictionary
    di = defaultdict(int)
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file, di)
    Report(di)
