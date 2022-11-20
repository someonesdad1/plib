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
        import string
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
          they are found.

          An acronym is defined as a sequence of capital letters and
          digits.  Use -m and -n to specify the length.
        Options:
            -m m    Define the minimum length of an acronym [{d['-m']}]
            -n n    Define the maximum length of an acronym [{d['-n']}]
            -s      Print the tokens in sorted order (also implies -u)
            -u      Print the unique tokens in the order they are found
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-m"] = 2
        d["-n"] = 5
        d["-s"] = False
        d["-u"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "hm:n:su") 
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
            if o == "-m":
                d["-m"] = m = int(a)
                if n < 1:
                    Error("-m option must be > 0")
            elif o == "-h":
                Usage(status=0)
        if d["-m"] > d["-n"]:
            d["-m"], d["-n"] = d["-n"], d["-m"] 
        return files
if 1:   # Core functionality
    def IsToken(s):
        'Must be all uppercase letters and numbers'
        for i in set(s):
            if i not in IsToken.characters:
                return False
        return True
    # Make IsToken container for allowed characters
    uc, dig = string.ascii_uppercase, string.digits
    IsToken.characters = set(uc + dig)
    def PrintTokens(stream):
        found = set()
        for token in GetTokens(stream):
            if not IsToken(token) or token[0] not in uc:
                continue
            if not (d["-m"] <= len(token) <= d["-n"]):
                continue
            if token.upper() == token:
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

