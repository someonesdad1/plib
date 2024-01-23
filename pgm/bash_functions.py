'''
Find bash shell functions in text
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
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        ii = isinstance
        g.func = set()
        g.myfunc = set()
if 1:   # Utility
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
          -d option.
        Options:
            -d file Define a default function file
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = []        # Default function file
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-d":
                file = P(a)
                if not file.exists():
                    Error(f"{a!r} doesn't exist")
                d[o].append(file)
            elif o == "-h":
                Usage(status=0)
        return args
if 1:   # Core functionality
    def GetFunctionName(line):
        'Use regexps to find a function definition line'
        if not GetFunctionName.regexps:
            r = GetFunctionName.regexps
            # Compile/cache regexps to identify a function
            # This form is what I use in my function definitions.  Note the
            # parentheses are optional.
            r.add(re.compile(r"^function ([A-Za-z_][A-Za-z0-9_]*)\s*(\(\s*\))?$"))
            # The following is the form of a function name output by bash's
            # set command
            r.add(re.compile(r"^([A-Za-z_][A-Za-z0-9_]*) \(\) $"))
    GetFunctionName.regexps = set()
    def GetFunctions(file, dictionary):
        pass

if 1:
    # This is a non-strict regexp and it matches things that are taken as
    # functions by bash.
    r = r"^\s*function\s+([a-z_][a-z0-9_]*)\s*(\(\s*\))\s*$|^\s*([a-z_][a-z0-9_]*)\s*(\(\s*\))\s*$"
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
    if d["-d"]:
        for file in d["-d"]:
            GetFunctions(file, g.my_func)
    args = ParseCommandLine(d)
