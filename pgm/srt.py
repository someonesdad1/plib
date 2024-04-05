'''
Sort the fields of each line of a text file
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
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        import get
        from wrap import dedent
        from wsl import wsl     # wsl is True when running under WSL Linux
        from lwtest import Assert
        #from columnize import Columnize
    if 1:   # Global variables
        class G:    # Storage for global variables as attributes
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
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        '''.rstrip()).lstrip())
        exit(0)
    def Usage():
        print(dedent(f'''
 
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Sort the fields of each line of a text file and send to stdout.  Tabs and other
          whitespace characters will be replaced by space characters if -f is not used.  Use "-"
          for stdin.
        Options:
            -f s    Define field separator [whitespace]
            -r      Reverse sort order
            -x re   Define regex for lines to ignore
 
        '''.rstrip()).lstrip())
        exit(0)
    def ParseCommandLine(d):
        d["-f"] = None      # Field separator (defaults to whitespace)
        d["-r"] = False     # Reverse sort order
        d["-x"] = []        # Sequences of regexes for ignoring lines
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "f:rx:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("r"):
                d[o] = not d[o]
            elif o == "-f":
                d[o] = a
            elif o == "-x":
                try:
                    d[o].append(re.compile(a))
                except Exception:
                    Error(f"{o!r} is not a valid regex")
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Core functionality
    def Ignore(line):
        'Return True if this line should be ignored'
        for r in d["-x"]:
            mo = r.search(line)
            if mo:
                return True
        return False
    def Process(file):
        'Sort the fields of each line in file'
        s = get.GetText(file)
        if s[-1] == "\n":
            s = s[:-1]  # Remove last newline to avoid a phantom last empty line
        for line in s.split("\n"):
            if Ignore(line):
                print(line)
                continue
            if d["-f"]:
                fields = line.split(d["-f"])
                fields = reversed(sorted(fields)) if d["-r"] else sorted(fields)
                print(d["-f"].join(fields))
            else:
                fields = line.split()
                fields = reversed(sorted(fields)) if d["-r"] else sorted(fields)
                print(' '.join(fields))

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        Process(file)
