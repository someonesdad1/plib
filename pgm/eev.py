'''
Search eevblog stuff for keywords
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
        from string import digits
        import sys
    if 1:   # Custom imports
        from eevblog_data import eevblog    # Dictionary of titles & URLs
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from util import Winnow
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.eev_num = re.compile(r"^EEVblog #?(\d{1, 4}) -")
        ii = isinstance
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
        Usage:  {sys.argv[0]} [options] regex1 [regex2...]
          Search for EEVblog titles that match the given regular expressions.  The regexes are
          AND'd together unless you use the -n option to OR them together.
        Options:
            -i      Do not ignore case in searches
            -n      OR the regexes
            -o      Open the URLs that are found
            -r      Print out in most-recent-first order
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Open URLs that are found
        d["-i"] = False     # Do not ignore case
        d["-o"] = False     # OR the regexes
        d["-r"] = False     # Most recent first order
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dio") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dio"):
                d[o] = not d[o]
        return args
if 1:   # Core functionality
    def GetCandidates(regexps):
        'Return a set of the titles to open'
        titles_to_search = list(eevblog)
        ignore_case = 0 if d["-i"] else re.I
        OR = True if d["-o"] else False
        titles = Winnow(titles_to_search, regexps, OR=OR, flags=ignore_case)
        return titles
    def SortKey(item):
        "Return the EEVblog number as int if it's there else 0"
        item = item.lower()
        if item.startswith("eevblog "):
            s = item.replace("eevblog ", "")
            if s and s[0] == "#":
                s = s[1:]
            # Get leading digits
            u = ""
            while s[0] in digits:
                u += s[0]
                s = s[1:]
            return int(u) if u else 0
        else:
            return 0
    def FormatTitle(title):
        "Remove 'EEVblog <num> -' stuff and replace with 'num: '"
        num = SortKey(title)
        if not num:
            return title

                
if __name__ == "__main__":
    d = {}      # Options dictionary
    regexps = ParseCommandLine(d)
    candidates = GetCandidates(regexps)
    results = []
    for i in sorted(candidates, key=SortKey):
        results.append(f"{i}")
    if d["-r"]:
        results = reversed(results)
    for i in results:
        print(i)
