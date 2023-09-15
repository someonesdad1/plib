'''
Delete blank lines from files or stdin
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Delete blank lines from files or stdin
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
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
          Delete blank lines from files.  Use '-' for stdin.
        Options:
            -1      Collapse multiple blank lines to one
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-1"] = False     # Multiple blank lines to one
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "1") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("1"):
                d[o] = not d[o]
        return files
if 1:   # Core functionality
    def ProcessFile(file):
        s = sys.stdin.read() if file == "-" else open(file).read()
        # Remove leading and trailing blank lines
        s = re.sub(r"^\n+", "", s)
        s = re.sub(r"\n+$", "", s)
        if d["-1"]:
            s = re.sub(r"\n\n\n+", "\n\n", s)
        else:
            s = re.sub(r"\n\n+", "\n", s)
        print(s)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)
