'''
Find bash shell functions in text
'''
from __future__ import annotations
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
        from pprint import pprint as pp
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from get import GetLines
        from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        g.funcs = set()
        g.myfuncs = set()
        # Regexps for matching bash function lines
        g.relaxed = re.compile(r"^\s*function\s+([a-z_][a-z0-9_]*)\s*(\(\s*\))\s*$|^\s*([a-z_][a-z0-9_]*)\s*(\(\s*\))\s*$")
        g.strict = re.compile(r"^function ([a-z_][a-z0-9_]*) *$")
if 1:   # Utility
    def GetColors():
        t.dbg = t("lill") if g.dbg else ""
        t.don = t("grnl")
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    g.W, g.L = GetScreen()
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
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Read files and find shell function names.  Use - for stdin.
          Print out a colorized alphabetized listing; a name in color is
          one that is defined in one or more function files defined by the
          -d option.  Use -r to define sets of functions that should be
          ignored (for example, git adds around 130 functions to your bash
          environment).
        Options:
            -c      Don't print columnized
            -d file Debug printing
            -f file Define a default function file
            -g      Ignore git & gawk functions
            -r file Define a ignore function file
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Columnized printing
        d["-d"] = False     # Debug printing
        d["-f"] = []        # Default function files
        d["-g"] = False     # Ignore git & gawk functions
        d["-r"] = []        # Default ignore files
        d["-s"] = False     # Use a strict regexp
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cdf:ghs") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cdgs"):
                d[o] = not d[o]
            elif o == "-f":
                file = P(a)
                if not file.exists():
                    Error(f"{a!r} doesn't exist")
                d[o].append(file)
            elif o == "-h":
                Usage(status=0)
        g.dbg = d["-d"]
        GetColors()
        return args
if 1:   # Core functionality
    def IgnoreGitGawk(item):
        'Return True if this is a git or gawk item'
        return (item.startswith("__git") or
                item.startswith("_git") or
                item.startswith("gawk"))
    def Report():
        'Print the function report'
        sentinel = None
        dq = deque(sorted(g.funcs))
        dq.append(sentinel)
        # Decorate those in g.myfuncs with color
        while dq:
            item = dq.popleft()
            if item is None:
                break
            if d["-g"] and IgnoreGitGawk(item):
                continue
            else:
                if item in g.myfuncs:
                    # Decorate with color
                    dq.append(f"{t.don}{item}{t.n}")
                else:
                    dq.append(item)
        if d["-c"]:
            for i in Columnize(dq):
                print(i)
        else:
            while dq:
                print(dq.popleft())
    def DebugPrint(funcs: set, lines: list):
        if g.dbg:
            if 0:
                for line in lines:
                    Dbg(line)
            Dbg(f"file = {str(file)!r}:  {len(lines)} lines")
            for i in Columnize(funcs):
                Dbg(i)
    def GetFunctions(file: Path, funcs: set, strict: bool):
        r = g.strict if strict else g.relaxed
        lines = GetLines(file, nonl=True)
        for line in lines:
            mo = r.match(line)
            if mo:
                dq = deque(mo.groups())
                while dq and dq[0] is None:
                    dq.popleft()
                assert dq
                funcs.add(dq.popleft())
        DebugPrint(funcs, lines)

print("xx Add -i option which lets you ignore starting prefixes; remove -g")
exit()

if 0:
    # This is a non-strict regexp and it matches things that are taken as
    # functions by bash.
    r = r"^\s*function\s+([a-z_][a-z0-9_]*)\s*(\(\s*\))\s*$|^\s*([a-z_][a-z0-9_]*)\s*(\(\s*\))\s*$"
    print(type(re.compile(r)));exit()
    S = '''
ab ()
cd	(	)		
	ef	(	)		
    '''
    for line in S.split("\n"):
        mo = re.match(r, line, re.I)
        if mo:
            print(f"{line!r}", mo.groups()[2])
        else:
            print(f"{line!r}", None)
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if d["-f"]:
        for file in d["-f"]:
            GetFunctions(file, g.myfuncs, True)
    for file in files:
        GetFunctions(file, g.funcs, False)
    Report()
