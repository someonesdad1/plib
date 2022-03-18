'''
Prints out combinations & permutations of command line arguments.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
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
    import pathlib
    import sys
    from itertools import combinations, permutations
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from clr import Clr
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    c = Clr()
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] A [B...]
            Prints out combinations & permutations of command line arguments.
            a is a string and if the only argument, then its letters are
            used as the elements.  Otherwise the set (A, B, ...) is used
            as the set.
        Notation
            n = number of letters in a or number of arguments if > 1
            k = items to take for each subset
            C(n, k) = combinations of n objects taken k at a time
            P(n, k) = all permutations of the size k subsets taken from
                      all the n elements
        Options (default in square brackets):
            -h      Print a manpage
            -k      Number of objects in C(n, k) or P(n, k)
            -s x    Separator string for grouped items [""]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
