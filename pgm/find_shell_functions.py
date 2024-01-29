'''

Purpose:  locate valid shell function definitions
    - Default behavior is to list all function names found


Find shell functions in text
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
        # Find shell functions in text
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
        # This will contain the function names found
        g.functions = set()
        if 1:   # Regexps for matching bash function lines
            # g.relaxed matches any valid function definition
            g.relaxed = re.compile(r"^\s*function\s+([A-Za-z_.][A-Za-z0-9_.]*)\s*(\(\s*\))\s*(#.*)?$|"
                                r"^\s*([A-Za-z_.][A-Za-z0-9_.]*)\s*(\(\s*\))\s*(#.*)?$")
            # g.strict matches function definitions that match my preferred # form
            g.strict = re.compile(r"^function ([a-z_][a-z0-9_]*) *(#.*)?$")
            # g.ignore contains regexps to ignore
            g.ignore = set()
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
          Print each function name found on one line.  Use -c to print in
          columns.
 
          The options -s and -S are used to identify functions that
          follow my preferred shell function forms:
            -s      "^function name$"
            -S      "^ *function name$"
 
        Note
          Bash function names can be any unquoted shell word without '$'.
          In this script, I only allow characters 'A-Z', 'a-z', '0-9', '_'
          and '.'.
        Options:
            -c      Print in columns
            -d      Debug printing
            -I r    Define regex for function names to ignore (case insensitive)
            -i r    Define regex for function names to ignore
            -s      Use strict regex to find my preferred function syntax
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Columnized printing
        d["-d"] = False     # Debug printing
        d["-i"] = []        # Function name regexes to ignore
        d["-s"] = False     # Use a strict regexp to find my preferred form
        d["ignore_regexps"] = []
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cdhi:s") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cds"):
                d[o] = not d[o]
            elif o in ("-i", "-I"):
                try:
                    if o == "-i":
                        d["ignore_regexps"].append(re.compile(a))
                    else:
                        d["ignore_regexps"].append(re.compile(a, re.I))
                except Exception as e:
                    print(f"Exception: {e!r}")
                    Error(f"  {a!r} not a proper regular expression for {o!r}")
                d[o].append(file)
            elif o == "-h":
                Usage(status=0)
        g.dbg = d["-d"]
        GetColors()
        return args
if 1:   # Core functionality
    def Report(function_set):
        'Print the function report'
        sentinel = None
        dq = deque(sorted(function_set))
        dq.append(sentinel)     # Identifies end of deque
        results = []
        while dq:
            funcname = dq.popleft()
            if funcname is sentinel:
                break
            # See if this funcname is to be ignored

            print(funcname)
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
    def DebugPrint(funcs, lines):
        '''funcs is a set, lines is a list
        '''
        if g.dbg:
            if 0:
                for line in lines:
                    Dbg(line)
            Dbg(f"file = {str(file)!r}:  {len(lines)} lines")
            Dbg(f"  File's functions:")
            for i in Columnize(funcs):
                Dbg(i)
    def GetFunctions(file, funcs, strict):
        r = g.strict if strict else g.relaxed
        Dbg(f"strict = {strict}")
        Dbg(f"regex = {r}")
        lines = GetLines(file, nonl=True)
        for line in lines:
            Dbg(f"{t('trql')}line = {line!r}")
            mo = r.match(line)
            if mo:
                Dbg("Matched")
                # The groups() list will contain a number of Nones, which
                # are followed by the function's name. 
                dq = deque(mo.groups())
                while dq and dq[0] is None:
                    dq.popleft()
                assert dq
                funcs.add(dq.popleft())
        DebugPrint(funcs, lines)

        exit() #xx

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
    strict = d["-s"]
    for file in files:
        GetFunctions(file, g.functions, strict)
    Report(g.functions)
