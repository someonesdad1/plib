'''
Find acronyms in a text file
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Find acronyms in a text file.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from get import GetTokens
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
          Print out acronyms found in the files on the command line.  Use
          '-' to read from stdin.  The tokens are printed out in the order
          they are found and duplicates are allowed.
        Options:
            -h      Print a manpage
            -n n    Define the maximum length of an acronym [{d['-n']}]
            -s      Print the tokens in sorted form (also implies -u)
            -u      Print the unique tokens
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-n"] = 5
        d["-s"] = False
        d["-u"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "hn:su") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("su"):
                d[o] = not d[o]
            if o == "-n":
                d["-n"] = n = int(a)
                if n < 1:
                    Error("-n option must be > 0")
            elif o == "-h":
                Usage(status=0)
        return files
if 1:   # Core functionality
    def PrintTokens(stream):
        found = set()
        for token in GetTokens(stream):
            if token.upper() == token:
                if len(token) > d["-n"]:
                    continue
                if d["-u"] or d["-s"]:
                    if token not in found:
                        if not d["-s"]:
                            print(token)
                else:
                    if not d["-s"]:
                        print(token)
                found.add(token)
        if d["-s"]:
            for i in sorted(found):
                print(i)


if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        if file == "-":
            PrintTokens(sys.stdin)
        else:
            try:
                stream = open(file)
            except Exception:
                Error(f"Couldn't open {file!s}")
            PrintTokens(open(file))

