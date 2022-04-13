'''
Generate short hash strings for files
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Generate short hash strings for files
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    # Standard imports
        import getopt
        import hashlib
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from wrap import wrap, dedent
        from clr import Clr
    # Global variables
        ii = isinstance
        c = Clr()
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Generate short hash strings for files.  The SHA-1 hash is used by
          default (same as git).
        Options:
            -1      Use MD5
            -n n    Print out n characters of the hash [{d["-n"]}]
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-1"] = False     # Use MD5
        d["-n"] = 5         # Number of hash digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "1hn:", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("1"):
                d[o] = not d[o]
            elif o in ("-n",):
                    d[o] = max(abs(int(a)), 2)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def ProcessFile(file):
        hash = hashlib.md5 if d["-1"] else hashlib.sha1
        h = hash()
        h.update(open(file, "rb").read())
        w = d["-n"]
        s = h.hexdigest()[:w].rstrip()
        w = min(w, len(s))
        print(f"{s:{w}s} {file}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)
