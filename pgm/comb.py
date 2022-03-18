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
    from columnize import Columnize
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
            Prints out combinations of command line arguments.  a is a
            string and if the only argument, then its letters are used as
            the elements.  Otherwise the set of n arguments (A, B, ...) is
            used.
        Notation
            n = number of letters in a or number of arguments if > 1
            k = items to take for each subset
            P(n, k) = all permutations of the size k subsets taken from
                      all the n elements
                    = n!/(n - k)!
            P(n)    = P(n, n) = n!
            C(n, k) = combinations of n objects taken k at a time
                    = P(n, k)/k!
        Options (default in square brackets):
            -c      Don't print in columns
            -h      Print a manpage
            -k k    Number of objects in C(n, k) or P(n, k) [1]
            -p      Print permutations P
            -s x    Separator string for grouped items [""]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Print in columns
        d["-k"] = None      # Choose number
        d["-p"] = False     # Print permutations
        d["-s"] = ""        # Separator string
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chk:ps:", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        global n, k
        n = len(args[0]) if len(args) == 1 else len(args)
        for o, a in opts:
            if o[1] in list("cp"):
                d[o] = not d[o]
            elif o == "-k":
                d[o] = k = int(a)
                if k < 1 or k > n:
                    Error(f"k must be between 1 and {n}")
            elif o == "-k":
                d[o] = a
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def Work(func, name, objects):
        k, count = d["-k"], 0
        if k is None and func == combinations:
            Error(f"Must use -k option with {name}")
        out = []
        for i in func(objects, k):
            out.append(d["-s"].join(i))
            count += 1
        if d["-c"]:
            for i in Columnize(out):
                print(i)
        else:
            for i in out:
                print(out)
        print(f"{count} {name}")

if __name__ == "__main__":
    n, k = None, None
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    objects = list(args[0]) if len(args) == 1 else args
    if d["-p"]:
        Work(permutations, "permutations", objects)
    else:
        Work(combinations, "combinations", objects)
