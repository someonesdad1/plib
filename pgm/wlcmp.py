'''
Compare files as wordlists
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
        # Compare files as wordlists
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from itertools import combinations
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
        from get import GetLines
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
        t.err = t("redl")
        t.dbg = t("cyn")
        t.ti = t("ornl")
        t.f1 = t("yell")
        t.f2 = t("purl")
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
 
        Usage:  {sys.argv[0]} [options] file1 file2 [file3...]
          Compare the files as wordlists.  The files will be selected in pairs and the comparison
          numbers printed for each pair.
        Options:
            -i      Do not ignore case of words
 
        '''.rstrip()).lstrip())
        exit(0)
    def ParseCommandLine(d):
        d["-i"] = False     # Do not ignore case
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "i") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Core functionality
    def GetWords(file):
        lines = GetLines(file, script=True, ignore_empty=True, strip=True, nonl=True)
        if not d["-i"]:
            lines = [i.lower() for i in lines]
        words = set((' '.join(lines)).split())
        return words
    def Analyze(file1, file2):
        s1 = GetWords(file1)
        s2 = GetWords(file2)
        sp = " "*2
        w = 6
        t.print(f"{t.ti}Comparing files {t.f1}{file1} ({len(s1)} words) {t.ti}and {t.f2}{file2} ({len(s2)} words)")
        print(f"{len(s1|s2):{w}d} {sp} Union")
        print(f"{len(s1&s2):{w}d} {sp} Intersection")
        n = len(s1 - s2)
        t.print(f"{n:{w}d} {sp} Words only in {t.f1}{file1}{t.n}")
        n = len(s2 - s1)
        t.print(f"{n:{w}d} {sp} Words only in {t.f2}{file2}{t.n}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if len(files) < 2:
        Usage()
    for file1, file2 in combinations(files, 2):
        Analyze(file1, file2)
