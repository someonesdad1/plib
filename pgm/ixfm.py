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
        t.output = t("purl")
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
            t.print(f"{t.err}{s!r} is empty")
            return False
        for i in s:
            if i not in digits:
                t.print(f"{t.err}{s!r} is not all digits")
                return False
        return True
    def Tminus(s):
        a = dict(zip("0123456789", "0987654321"))
        return ''.join(a[i] for i in s)
    def IsOdd(n):
        assert(ii(n, int) and n > 0)
        return bool(n % 2 != 0)
    def TenRev(s):
        'Reverse digits, subtract each from 10, 0 -> 0'
        if not AllDigits(s):
            return
        return Tminus(list(reversed(str(s))))
    TenRev.description = "Reverse digits, 10 - d, 0 -> 0"
    TenRev.alg = "TenRev"
    def TenTwin(s):
        'Reverse adjacent digits, subtract each from 10, 0 -> 0'
        if not AllDigits(s):
            return
        lst = list(s)
        n = len(lst)
        for i in range(0, n - IsOdd(n), 2):
            lst[i], lst[i + 1] = lst[i + 1], lst[i]
        return Tminus(lst)
    TenTwin.description = "Reverse adjacent digits, 10 - d, 0 -> 0"
    TenTwin.alg = "TenTwin"
if 1:   # Core functionality
    def PrintResults():
        # Get max column widths
        w0, w1 = 10, 10
        for s0, s1 in g.results:
            w0 = max(w0, len(s0))
            w1 = max(w1, len(s1))
        # Print the algorithm used
        f = g.algorithms[d["-a"]]
        print(f"Used algorithm {f.alg!r}\n")
        # Print the header
        t.print(f"{'In':^{w0}s} {t.output}{'Out':^{w1}s}")
        t.print(f"{'-'*w0:s} {t.output}{'-'*w1:s}")
        # Print the data
        for input, output in g.results:
            t.print(f"{input!s:^{w0}s} {t.output}{output!s:^{w1}s}")
    def Transform(s):
        f = g.algorithms[d["-a"]]
        result = f(s)
        if result is not None:
            g.results.append((s, result))

if __name__ == "__main__":
    d = {}      # Options dictionary
    g.algorithms = [
        TenTwin,
        TenRev,
    ]
    g.results = []
    args = ParseCommandLine(d)
    for i in args:
        Transform(i)
    PrintResults()
