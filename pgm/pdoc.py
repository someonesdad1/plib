'''
Display python files without header information
    
    The default behavior is to search for lines with "#∞x∞#" were x is one of the keywords
    copyright, contact, category, license, what, and test.  

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
        # Display python files without header information
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
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("ornl")
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
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [arg1 [arg2...]]
          Examine the arguments (assumed to be python files) and print out those that need 
          work.  The goal is to 
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-r"] = False     # Recursively search for python scripts
        if 0 and len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hr") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("r"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Classes
    class File:
        def __init__(self, file, lines):
            self.file = file
            self.lines = lines
            # Attributes
            self.copyright = 0
            self.contact = 0
            self.license = 0
            self.what = 0
            self.test = 0
            self.category = 0
            # Get the keywords
            for line in lines:
                line = line.strip()
                if line.startswith("#∞copyright∞#"):
                    self.copyright += 1
                    Assert(line.endswith("#∞copyright∞#"))
                elif line.startswith("#∞contact∞#"):
                    self.contact += 1
                    Assert(line.endswith("#∞contact∞#"))
                elif line.startswith("#∞license∞#"):
                    self.license += 1
                elif line.startswith("#∞what∞#"):
                    self.what += 1
                elif line.startswith("#∞test∞#"):
                    self.test += 1
                    Assert(line.endswith("#∞test∞#"))
                elif line.startswith("#∞category∞#"):
                    self.category += 1
                else:
                    Error(f"{line!r} not recognized")
        def check(self):
            'Verify the #∞...∞# attributes are correct'
            errors = []
            if not self.copyright:
                errors.append("Missing '#∞copyright∞#'")
            elif not self.contact:
                errors.append("Missing '#∞contact∞#'")
            elif self.license != 2:
                errors.append("Must have two '#∞license∞#' on separate lines")
            elif self.what != 2:
                errors.append("Must have two '#∞what∞#' on separate lines")
            elif not self.test:
                errors.append("Missing '#∞test∞#'")
            elif not self.category:
                errors.append("Missing '#∞category∞#'")
            if errors:
                t.print(f"{t.err}{self.file} errors:")
                for e in errors:
                    print(f"  {e}")

if 1:   # Core functionality
    def Process(i):
        p = P(i)
        if p.is_dir():
            if d["-r"]:
                files = p.glob("**/*.py")
            else:
                files = p.glob("*.py")
        elif p.is_file():
            files = [p]
        else:
            Error(f"{i!r} is not a file or directory")
        # Process each file
        r1 = re.compile(r"^[^#]*$")
        s = "|".join("copyright contact license what test category".split())
        r2 = re.compile(f"^ *#∞({s})∞#")
        for file in files:
            lines = GetLines(file, ignore=[r1], ignore_empty=True, nonl=True)
            keep = [i.strip() for i in lines if r2.search(i)]
        f = File(file, keep)
        f.check()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        breakpoint() #xx 
    else:
        for i in args:
            Process(i)
