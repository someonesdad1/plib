'''
Script to aid the H() shell function in getting the required directory.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Script aid for the H() shell function.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [number]
          Returns the line from the config file indicated by number.
          Defaults to {d["number"]}.
        Options:
          -c f    Specify the config file.  [{d["-c"]}]
          -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = P("~/.curdir")
        d["number"] = 1
        try:
            opts, args = getopt.getopt(sys.argv[1:], "c:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-c",):
                d["-c"] = P(a)
                if not d["-c"].exists():
                    print("'{d['-c']}' doesn't exist")
            elif o in ("-h", "--help"):
                Usage(status=0)
        if not args:
            args = ["1"]
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    number = ParseCommandLine(d)[0]
    if number.lower() == "e":
        # Edit the config file
    else:
        print("Number =", int(number))
