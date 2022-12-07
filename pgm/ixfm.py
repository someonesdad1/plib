'''
Transform an integer
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
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        from string import digits
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
        ii = isinstance
        class g: pass
        t.err = t("redl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] str1 [str2...]
          Transform the integer(s) in the string(s) to "shrouded" values.
        Options:
            -a n    Choose the algorithm [{d['-a']}]
            -l      List the algorithms
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = 0         # Choose the algorithm
        d["-l"] = False     # List the algorithms
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "a:hl") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("l"):
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
            elif o == "-h":
                Usage(status=0)
        if d["-l"]:
            ListAlgorithms()
        return args
if 1:   # Algorithms
    def ListAlgorithms():
        print(dedent(f'''
        0:  Default algorithm ("Ten hut")
            Only works on strings with integers.  Reverse the string and
            subtract each digit from 10.  0 is left unchanged.  Intended to
            be used on phone numbers, door lock codes, etc.
        1:  ROT13
        '''))
        exit(0)
    def AllDigits(s):
        if not s:
            return False
        for i in s:
            if i not in digits:
                return False
        return True
    def TenHut(s):
        'Reverse digits, subtract each from 10, 0 -> 0'
        if not AllDigits(s):
            t.print(f"{t.err}{s!r} is not all digits")
            return
        a = dict(zip("0123456789", "0987654321"))
        r = [a[i] for i in  list(reversed(str(s)))]
        return ''.join(r)
    TenHut.description = "Reverse digits, 10 - d, 0 -> 0"
    def TenTwin(s):
        'Reverse adjacent digits, subtract each from 10, 0 -> 0'
        a = dict(zip("0123456789", "0987654321"))
        r = [a[i] for i in  list(reversed(str(s)))]
        return ''.join(r)
    TenTwin.description = "Reverse adjacent digits, 10 - d, 0 -> 0"
if 1:   # Core functionality
    def PrintResults():
        for input, output in g.results:
            print(input, output)
    def Transform(s):
        f = g.algorithms[d["-a"]]
        result = f(s)
        if result is not None:
            g.results.append((s, result))

if __name__ == "__main__":
    d = {}      # Options dictionary
    g.algorithms = [
        TenHut,
        TenTwin,
    ]
    g.results = []
    args = ParseCommandLine(d)
    for i in args:
        Transform(i)
    PrintResults()
